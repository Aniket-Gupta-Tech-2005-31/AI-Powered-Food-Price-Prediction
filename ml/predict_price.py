import os
import sys
import logging
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Add project path
sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from api.models import PriceEntry, Prediction, Vegetable, City
from django.utils import timezone

logger = logging.getLogger(__name__)


def load_model(model_path):
    """Load a pickled model"""
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        logger.error(f"Error loading model from {model_path}: {e}")
        return None


def predict_with_prophet(model, periods=30):
    """Generate predictions using Prophet model"""
    try:
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)

        predictions = []
        for idx, row in forecast.iterrows():
            if row['ds'].date() > datetime.now().date():
                predictions.append({
                    'date': row['ds'].date(),
                    'predicted_price': max(0, row['yhat']),
                    'lower_bound': max(0, row['yhat_lower']),
                    'upper_bound': max(0, row['yhat_upper']),
                    'confidence': 0.85
                })

        return predictions

    except Exception as e:
        logger.error(f"Error predicting with Prophet: {e}")
        return []


def predict_with_arima(model, periods=30):
    """Generate predictions using ARIMA model"""
    try:
        forecast = model.get_forecast(steps=periods)
        predictions_df = forecast.conf_int()

        predictions = []
        for i in range(periods):
            predicted_price = forecast.predicted_mean.iloc[i]
            lower = predictions_df.iloc[i, 0]
            upper = predictions_df.iloc[i, 1]

            predictions.append({
                'date': datetime.now().date() + timedelta(days=i+1),
                'predicted_price': max(0, float(predicted_price)),
                'lower_bound': max(0, float(lower)),
                'upper_bound': max(0, float(upper)),
                'confidence': 0.80
            })

        return predictions

    except Exception as e:
        logger.error(f"Error predicting with ARIMA: {e}")
        return []


def ensemble_predictions(prophet_preds, arima_preds):
    """
    Combine predictions from multiple models using ensemble method
    """
    if not prophet_preds or not arima_preds:
        return prophet_preds or arima_preds

    ensemble = []
    for i in range(min(len(prophet_preds), len(arima_preds))):
        avg_price = (prophet_preds[i]['predicted_price'] + arima_preds[i]['predicted_price']) / 2
        avg_confidence = (prophet_preds[i]['confidence'] + arima_preds[i]['confidence']) / 2

        ensemble.append({
            'date': prophet_preds[i]['date'],
            'predicted_price': avg_price,
            'lower_bound': min(prophet_preds[i]['lower_bound'], arima_preds[i]['lower_bound']),
            'upper_bound': max(prophet_preds[i]['upper_bound'], arima_preds[i]['upper_bound']),
            'confidence': avg_confidence
        })

    return ensemble


def generate_predictions(vegetable_id, city_id, days=30, use_ensemble=True):
    """
    Generate price predictions and store in database
    """
    try:
        vegetable = Vegetable.objects.get(id=vegetable_id)
        city = City.objects.get(id=city_id)

        logger.info(f"Generating predictions for {vegetable.name} in {city.name}...")

        model_dir = Path(__file__).parent / 'models'

        # Load models
        prophet_path = model_dir / f'prophet_{vegetable.name}_{city.name}.pkl'
        arima_path = model_dir / f'arima_{vegetable.name}_{city.name}.pkl'

        prophet_model = load_model(prophet_path) if prophet_path.exists() else None
        arima_model = load_model(arima_path) if arima_path.exists() else None

        if not prophet_model and not arima_model:
            logger.warning(f"No trained models found for {vegetable.name} in {city.name}")
            return []

        # Generate predictions
        prophet_preds = predict_with_prophet(prophet_model, days) if prophet_model else []
        arima_preds = predict_with_arima(arima_model, days) if arima_model else []

        # Use ensemble or single model
        if use_ensemble and prophet_preds and arima_preds:
            predictions = ensemble_predictions(prophet_preds, arima_preds)
            model_used = 'ensemble'
        elif prophet_preds:
            predictions = prophet_preds
            model_used = 'prophet'
        else:
            predictions = arima_preds
            model_used = 'arima'

        # Store predictions in database
        for pred in predictions:
            Prediction.objects.update_or_create(
                vegetable=vegetable,
                city=city,
                prediction_date=pred['date'],
                defaults={
                    'predicted_price': pred['predicted_price'],
                    'model_used': model_used,
                    'confidence': pred['confidence'],
                    'lower_bound': pred['lower_bound'],
                    'upper_bound': pred['upper_bound']
                }
            )

        logger.info(f"Generated and stored {len(predictions)} predictions")
        return predictions

    except Exception as e:
        logger.error(f"Error in generate_predictions: {e}")
        return []


def batch_generate_predictions(days=30):
    """
    Generate predictions for all vegetable-city combinations
    """
    vegetables = Vegetable.objects.all()
    cities = City.objects.all()

    total_predictions = 0
    for vegetable in vegetables:
        for city in cities:
            preds = generate_predictions(
                vegetable_id=vegetable.id,
                city_id=city.id,
                days=days
            )
            total_predictions += len(preds)

    logger.info(f"Total predictions generated: {total_predictions}")
    return total_predictions
