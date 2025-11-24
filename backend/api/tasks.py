from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

from .models import City, Vegetable, PriceEntry, Prediction
from scraper.gov_api_fetch import fetch_government_prices
from scraper.online_store_scraper import fetch_online_store_prices
from scraper.clean_data import clean_price_data
from ml.predict_price import generate_predictions

logger = logging.getLogger(__name__)


@shared_task
def fetch_and_store_prices():
    """
    Celery task to fetch prices from multiple sources and store in database.
    Runs daily via beat schedule.
    """
    try:
        logger.info("Starting price fetch task...")

        # Fetch from government API
        gov_prices = fetch_government_prices()
        logger.info(f"Fetched {len(gov_prices)} prices from government API")

        # Fetch from online stores
        online_prices = fetch_online_store_prices()
        logger.info(f"Fetched {len(online_prices)} prices from online stores")

        # Combine and clean data
        all_prices = gov_prices + online_prices
        cleaned_prices = clean_price_data(all_prices)

        # Store in database
        count = 0
        for price_data in cleaned_prices:
            try:
                vegetable, _ = Vegetable.objects.get_or_create(
                    name=price_data['vegetable_name'],
                    defaults={'category': 'other'}
                )

                city, _ = City.objects.get_or_create(
                    name=price_data['city_name'],
                    defaults={'state': ''}
                )

                PriceEntry.objects.create(
                    vegetable=vegetable,
                    city=city,
                    price_per_kg=price_data['price_per_kg'],
                    source=price_data['source'],
                    location=price_data.get('location', ''),
                    quality_rating=price_data.get('quality_rating', 5)
                )
                count += 1
            except Exception as e:
                logger.error(f"Error storing price: {e}")
                continue

        logger.info(f"Stored {count} price entries successfully")
        return {'status': 'success', 'count': count}

    except Exception as e:
        logger.error(f"Error in fetch_and_store_prices: {e}")
        return {'status': 'error', 'message': str(e)}


@shared_task
def train_prediction_models():
    """
    Celery task to train ML models.
    Runs daily via beat schedule.
    """
    try:
        logger.info("Starting model training task...")

        # Get all vegetables and cities
        vegetables = Vegetable.objects.all()
        cities = City.objects.all()

        for vegetable in vegetables:
            for city in cities:
                try:
                    # Get historical prices
                    prices = PriceEntry.objects.filter(
                        vegetable=vegetable,
                        city=city
                    ).order_by('timestamp')

                    if prices.count() < 30:
                        logger.warning(
                            f"Insufficient data for {vegetable.name} in {city.name}"
                        )
                        continue

                    logger.info(
                        f"Training model for {vegetable.name} in {city.name}"
                    )
                    # Training happens in ml module
                    # This is a placeholder for the actual training logic

                except Exception as e:
                    logger.error(
                        f"Error training model for {vegetable.name}: {e}"
                    )
                    continue

        logger.info("Model training completed")
        return {'status': 'success'}

    except Exception as e:
        logger.error(f"Error in train_prediction_models: {e}")
        return {'status': 'error', 'message': str(e)}


@shared_task
def generate_predictions():
    """
    Celery task to generate price predictions.
    Runs daily via beat schedule.
    """
    try:
        logger.info("Starting prediction generation task...")

        vegetables = Vegetable.objects.all()
        cities = City.objects.all()

        for vegetable in vegetables:
            for city in cities:
                try:
                    predictions = generate_predictions(
                        vegetable_id=vegetable.id,
                        city_id=city.id,
                        days=30
                    )

                    logger.info(
                        f"Generated {len(predictions)} predictions for "
                        f"{vegetable.name} in {city.name}"
                    )

                except Exception as e:
                    logger.error(
                        f"Error generating predictions for {vegetable.name}: {e}"
                    )
                    continue

        logger.info("Prediction generation completed")
        return {'status': 'success'}

    except Exception as e:
        logger.error(f"Error in generate_predictions: {e}")
        return {'status': 'error', 'message': str(e)}
