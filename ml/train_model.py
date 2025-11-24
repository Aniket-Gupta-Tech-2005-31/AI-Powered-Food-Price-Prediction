import os
import sys
import logging
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

# Add project path
sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from api.models import PriceEntry, Prediction, Vegetable, City
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


def preprocess_price_data(prices):
    """
    Preprocess price data for model training
    """
    df = pd.DataFrame([{
        'date': p.timestamp.date(),
        'price': float(p.price_per_kg),
        'source': p.source,
        'quality': p.quality_rating
    } for p in prices])

    # Sort by date
    df = df.sort_values('date')

    # Handle missing values
    df = df.fillna(method='ffill').fillna(method='bfill')

    return df


def train_prophet_model(prices, vegetable_name, city_name):
    """
    Train Prophet model for price prediction
    """
    try:
        from prophet import Prophet

        df = preprocess_price_data(prices)

        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        prophet_df = pd.DataFrame({
            'ds': df['date'],
            'y': df['price']
        })

        # Initialize and fit Prophet model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            interval_width=0.95
        )

        model.fit(prophet_df)

        model_path = Path(__file__).parent / 'models' / f'prophet_{vegetable_name}_{city_name}.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        logger.info(f"Successfully trained Prophet model for {vegetable_name} in {city_name}")
        return model

    except Exception as e:
        logger.error(f"Error training Prophet model: {e}")
        return None


def train_arima_model(prices, vegetable_name, city_name):
    """
    Train ARIMA model for price prediction
    """
    try:
        from statsmodels.arima.model import ARIMA

        df = preprocess_price_data(prices)

        # Train ARIMA model
        model = ARIMA(df['price'], order=(1, 1, 1))
        fitted_model = model.fit()

        model_path = Path(__file__).parent / 'models' / f'arima_{vegetable_name}_{city_name}.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(fitted_model, f)

        logger.info(f"Successfully trained ARIMA model for {vegetable_name} in {city_name}")
        return fitted_model

    except Exception as e:
        logger.error(f"Error training ARIMA model: {e}")
        return None


def train_all_models(vegetable_id, city_id):
    """
    Train all available models for a vegetable-city combination
    """
    try:
        vegetable = Vegetable.objects.get(id=vegetable_id)
        city = City.objects.get(id=city_id)

        # Get historical prices
        prices = PriceEntry.objects.filter(
            vegetable=vegetable,
            city=city
        ).order_by('timestamp')

        if prices.count() < 30:
            logger.warning(f"Insufficient data for {vegetable.name} in {city.name}")
            return None

        logger.info(f"Training models for {vegetable.name} in {city.name}...")

        # Train Prophet
        prophet_model = train_prophet_model(prices, vegetable.name, city.name)

        # Train ARIMA
        arima_model = train_arima_model(prices, vegetable.name, city.name)

        return {
            'prophet': prophet_model,
            'arima': arima_model,
            'vegetable': vegetable.name,
            'city': city.name
        }

    except Exception as e:
        logger.error(f"Error in train_all_models: {e}")
        return None
