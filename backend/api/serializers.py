from rest_framework import serializers
from .models import City, Vegetable, PriceEntry, Prediction, UserFeedback


# ========== CITY SERIALIZER ==========
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'state', 'latitude', 'longitude']


# ========== VEGETABLE SERIALIZER ==========
class VegetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegetable
        fields = ['id', 'name', 'category', 'image_url', 'description']


# ========== PRICE ENTRY SERIALIZER ==========
class PriceEntrySerializer(serializers.ModelSerializer):
    vegetable_name = serializers.CharField(source='vegetable.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = PriceEntry
        fields = [
            'id',
            'vegetable',
            'vegetable_name',
            'city',
            'city_name',
            'price_per_kg',
            'source',
            'location',
            'timestamp',
            'quality_rating'
        ]


# ========== PREDICTION SERIALIZER ==========
class PredictionSerializer(serializers.ModelSerializer):
    vegetable_name = serializers.CharField(source='vegetable.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Prediction
        fields = [
            'id',
            'vegetable',
            'vegetable_name',
            'city',
            'city_name',
            'predicted_price',
            'prediction_date',
            'model_used',
            'confidence',
            'lower_bound',
            'upper_bound'
        ]


# ========== USER FEEDBACK SERIALIZER ==========
class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = ['id', 'feedback_type', 'vegetable', 'city', 'comment']
        read_only_fields = ['id', 'created_at']


# ========== CUSTOM RESPONSE SERIALIZERS ==========
class PriceComparisonSerializer(serializers.Serializer):
    source = serializers.CharField()
    location = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    timestamp = serializers.DateTimeField()


class RecommendationSerializer(serializers.Serializer):
    vegetable_name = serializers.CharField()
    current_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    predicted_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    action = serializers.CharField()  # 'Buy Now' or 'Wait'
    reason = serializers.CharField()
    potential_savings = serializers.DecimalField(max_digits=8, decimal_places=2)
    confidence = serializers.FloatField()


class PredictionDataSerializer(serializers.Serializer):
    date = serializers.DateField()
    predicted_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    lower_bound = serializers.DecimalField(max_digits=8, decimal_places=2)
    upper_bound = serializers.DecimalField(max_digits=8, decimal_places=2)
    confidence = serializers.FloatField()


class InsightSerializer(serializers.Serializer):
    item_name = serializers.CharField()
    avg_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    min_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    trend = serializers.FloatField()  # -1 to 1, where -1 is falling, 0 is stable, 1 is rising


class SavingsSummarySerializer(serializers.Serializer):
    total_savings = serializers.DecimalField(max_digits=10, decimal_places=2)
    items_saved = serializers.IntegerField()
    recommendations_followed = serializers.IntegerField()
