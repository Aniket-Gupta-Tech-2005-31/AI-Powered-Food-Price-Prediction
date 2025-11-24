from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Min, Max, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import City, Vegetable, PriceEntry, Prediction
from .serializers import (
    CitySerializer,
    VegetableSerializer,
    PriceEntrySerializer,
    PredictionSerializer,
    PriceComparisonSerializer,
    RecommendationSerializer,
    PredictionDataSerializer,
    InsightSerializer,
    SavingsSummarySerializer,
)
import os
from rest_framework.permissions import IsAdminUser
from api.tasks import fetch_and_store_prices
from .serializers import PriceEntrySerializer


# ========== VIEWSETS ==========
class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class VegetableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vegetable.objects.all()
    serializer_class = VegetableSerializer


class PriceEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceEntry.objects.all()
    serializer_class = PriceEntrySerializer

    def get_queryset(self):
        queryset = PriceEntry.objects.all()
        city = self.request.query_params.get('city')
        vegetable = self.request.query_params.get('vegetable')

        if city:
            queryset = queryset.filter(city__name=city)
        if vegetable:
            queryset = queryset.filter(vegetable__name=vegetable)

        return queryset


class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

    def get_queryset(self):
        queryset = Prediction.objects.all()
        city = self.request.query_params.get('city')
        vegetable = self.request.query_params.get('vegetable')
        days = self.request.query_params.get('days', 7)

        if city:
            queryset = queryset.filter(city__name=city)
        if vegetable:
            queryset = queryset.filter(vegetable__name=vegetable)

        future_date = timezone.now().date() + timedelta(days=int(days))
        queryset = queryset.filter(prediction_date__lte=future_date)

        return queryset


# ========== CUSTOM API VIEWS ==========
class CurrentPricesView(APIView):
    """Get current prices for a city"""

    def get(self, request):
        city_name = request.query_params.get('city')

        if not city_name:
            return Response(
                {'error': 'City parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            return Response(
                {'error': f'City {city_name} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get latest prices for each vegetable
        latest_prices = []
        vegetables = Vegetable.objects.all()

        for vegetable in vegetables:
            # Get latest price entries from different sources
            latest = PriceEntry.objects.filter(
                vegetable=vegetable,
                city=city
            ).order_by('-timestamp')[:1]

            if latest.exists():
                entry = latest[0]
                # Get previous price for comparison
                previous = PriceEntry.objects.filter(
                    vegetable=vegetable,
                    city=city,
                    timestamp__lt=entry.timestamp
                ).order_by('-timestamp')[:1]

                price_change = 0
                if previous.exists():
                    prev_price = float(previous[0].price_per_kg)
                    curr_price = float(entry.price_per_kg)
                    price_change = ((curr_price - prev_price) / prev_price * 100) if prev_price != 0 else 0

                latest_prices.append({
                    'vegetable_name': vegetable.name,
                    'price_per_kg': float(entry.price_per_kg),
                    'source': entry.get_source_display(),
                    'city': city.name,
                    'timestamp': entry.timestamp,
                    'price_change': price_change,
                    'quality_rating': entry.quality_rating
                })

        return Response(latest_prices)


class ComparisonView(APIView):
    """Compare prices of a vegetable across sources"""

    def get(self, request):
        city_name = request.query_params.get('city')
        vegetable_name = request.query_params.get('item')
        state_name = request.query_params.get('state')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        sort = request.query_params.get('sort')  # 'price_asc' or 'price_desc'

        if not city_name or not vegetable_name:
            return Response(
                {'error': 'City and item parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            vegetable = Vegetable.objects.get(name=vegetable_name)
        except Vegetable.DoesNotExist:
            return Response({'error': 'Vegetable not found'}, status=status.HTTP_404_NOT_FOUND)

        # Build base queryset
        queryset = PriceEntry.objects.filter(vegetable=vegetable)

        # Filter by city or state if provided
        if city_name:
            queryset = queryset.filter(city__name=city_name)
        elif state_name:
            queryset = queryset.filter(city__state=state_name)

        # Date range filtering
        try:
            if start_date:
                from datetime import datetime
                sd = datetime.strptime(start_date, '%Y-%m-%d')
                queryset = queryset.filter(timestamp__date__gte=sd.date())
            if end_date:
                from datetime import datetime
                ed = datetime.strptime(end_date, '%Y-%m-%d')
                queryset = queryset.filter(timestamp__date__lte=ed.date())
        except Exception:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        # Default to last 7 days if no dates provided
        if not start_date and not end_date:
            from django.utils import timezone
            from datetime import timedelta
            end = timezone.now().date()
            start = end - timedelta(days=7)
            queryset = queryset.filter(timestamp__date__range=[start, end])

        # Convert queryset to list of dicts
        comparison_data = []
        for entry in queryset.order_by('source', '-timestamp'):
            comparison_data.append({
                'date': entry.timestamp.date().isoformat(),
                'source': entry.get_source_display(),
                'price': float(entry.price_per_kg),
                'city': entry.city.name,
                'location': entry.location,
                'quality_rating': entry.quality_rating,
            })

        # Optional sorting
        if sort == 'price_asc':
            comparison_data = sorted(comparison_data, key=lambda x: x['price'])
        elif sort == 'price_desc':
            comparison_data = sorted(comparison_data, key=lambda x: x['price'], reverse=True)

        return Response(comparison_data)


class PredictionDetailView(APIView):
    """Get price predictions for a vegetable"""

    def get(self, request):
        city_name = request.query_params.get('city')
        vegetable_name = request.query_params.get('item')
        days = int(request.query_params.get('days', 7))

        if not city_name or not vegetable_name:
            return Response(
                {'error': 'City and item parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            city = City.objects.get(name=city_name)
            vegetable = Vegetable.objects.get(name=vegetable_name)
        except (City.DoesNotExist, Vegetable.DoesNotExist):
            return Response(
                {'error': 'City or vegetable not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        today = timezone.now().date()
        future_date = today + timedelta(days=days)

        predictions = Prediction.objects.filter(
            vegetable=vegetable,
            city=city,
            prediction_date__gte=today,
            prediction_date__lte=future_date
        ).order_by('prediction_date')

        prediction_data = []
        for pred in predictions:
            prediction_data.append({
                'date': pred.prediction_date,
                'predicted_price': float(pred.predicted_price),
                'lower_bound': float(pred.lower_bound) if pred.lower_bound else None,
                'upper_bound': float(pred.upper_bound) if pred.upper_bound else None,
                'confidence': pred.confidence,
                'model_used': pred.get_model_used_display()
            })

        return Response(prediction_data)


class RecommendationView(APIView):
    """Generate buy/wait recommendations"""

    def get(self, request):
        city_name = request.query_params.get('city')

        if not city_name:
            return Response(
                {'error': 'City parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            return Response(
                {'error': 'City not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        recommendations = []
        vegetables = Vegetable.objects.all()

        for vegetable in vegetables:
            # Get current price
            current = PriceEntry.objects.filter(
                vegetable=vegetable,
                city=city
            ).order_by('-timestamp')[:1]

            if not current.exists():
                continue

            curr_price = float(current[0].price_per_kg)

            # Get prediction for next day
            tomorrow = timezone.now().date() + timedelta(days=1)
            prediction = Prediction.objects.filter(
                vegetable=vegetable,
                city=city,
                prediction_date=tomorrow
            ).first()

            if not prediction:
                continue

            pred_price = float(prediction.predicted_price)
            potential_savings = curr_price - pred_price

            # Determine action
            if pred_price < curr_price * 0.95:  # More than 5% drop expected
                action = 'Wait'
                reason = f'Price expected to drop to ₹{pred_price:.2f} tomorrow'
            else:
                action = 'Buy Now'
                reason = f'Price likely to increase or stay stable'

            recommendations.append({
                'vegetable_name': vegetable.name,
                'current_price': curr_price,
                'predicted_price': pred_price,
                'action': action,
                'reason': reason,
                'potential_savings': max(0, potential_savings),
                'confidence': prediction.confidence
            })

        return Response(recommendations)


class InsightsView(APIView):
    """Get market insights for a month"""

    def get(self, request):
        city_name = request.query_params.get('city')
        month_name = request.query_params.get('month', 'January')

        if not city_name:
            return Response(
                {'error': 'City parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            return Response(
                {'error': 'City not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Parse month (for demonstration, using current month)
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

        insights = []
        vegetables = Vegetable.objects.all()

        for vegetable in vegetables:
            prices = PriceEntry.objects.filter(
                vegetable=vegetable,
                city=city,
                timestamp__range=[month_start, month_end]
            )

            if prices.count() == 0:
                continue

            stats = prices.aggregate(
                avg_price=Avg('price_per_kg'),
                min_price=Min('price_per_kg'),
                max_price=Max('price_per_kg')
            )

            # Calculate trend
            first_half = prices[:prices.count() // 2]
            second_half = prices[prices.count() // 2:]

            first_avg = float(first_half.aggregate(Avg('price_per_kg'))['price_per_kg__avg'] or 0)
            second_avg = float(second_half.aggregate(Avg('price_per_kg'))['price_per_kg__avg'] or 0)

            if first_avg == 0:
                trend = 0
            else:
                trend = (second_avg - first_avg) / first_avg

            insights.append({
                'item_name': vegetable.name,
                'avg_price': float(stats['avg_price'] or 0),
                'min_price': float(stats['min_price'] or 0),
                'max_price': float(stats['max_price'] or 0),
                'trend': min(1, max(-1, trend))  # Normalize to -1 to 1
            })

        return Response(insights)


class FetchNowView(APIView):
    """Trigger a fetch of latest prices via scrapers.

    POST only. Requires header 'X-FETCH-KEY' matching env var FETCH_API_KEY.
    If allowed, enqueues the Celery task and returns task id.
    """

    def post(self, request):
        key = request.headers.get('X-FETCH-KEY') or request.data.get('fetch_key')
        env_key = os.getenv('FETCH_API_KEY')

        if not env_key:
            return Response({'error': 'Fetch endpoint not configured (FETCH_API_KEY missing)'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not key or key != env_key:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        # Enqueue task
        try:
            task = fetch_and_store_prices.delay()
            return Response({'status': 'enqueued', 'task_id': task.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitPriceView(APIView):
    """Allow users to submit price entries via POST.

    Accepts JSON with either `vegetable` (id) or `vegetable_name`, and `city` (id) or `city_name`.
    Required: price_per_kg
    Optional: source, location, quality_rating, timestamp
    """

    def post(self, request):
        data = request.data or {}

        veg_id = data.get('vegetable')
        veg_name = data.get('vegetable_name')
        city_id = data.get('city')
        city_name = data.get('city_name')
        price = data.get('price_per_kg')

        if price is None:
            return Response({'error': 'price_per_kg is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Resolve or create vegetable
        if veg_id:
            try:
                vegetable = Vegetable.objects.get(id=veg_id)
            except Vegetable.DoesNotExist:
                return Response({'error': 'Vegetable id not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if not veg_name:
                return Response({'error': 'vegetable or vegetable_name required'}, status=status.HTTP_400_BAD_REQUEST)
            vegetable, _ = Vegetable.objects.get_or_create(name=veg_name, defaults={'category': 'other'})

        # Resolve or create city
        if city_id:
            try:
                city = City.objects.get(id=city_id)
            except City.DoesNotExist:
                return Response({'error': 'City id not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if not city_name:
                return Response({'error': 'city or city_name required'}, status=status.HTTP_400_BAD_REQUEST)
            city, _ = City.objects.get_or_create(name=city_name, defaults={'state': ''})

        # Create price entry
        try:
            price_entry = PriceEntry.objects.create(
                vegetable=vegetable,
                city=city,
                price_per_kg=price,
                source=data.get('source', 'local'),
                location=data.get('location', ''),
                quality_rating=data.get('quality_rating', 3)
            )
            serializer = PriceEntrySerializer(price_entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
