"""
Script to populate sample prediction data for testing
"""
import os
import django
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import City, Vegetable, Prediction

def populate_predictions():
    """Add sample predictions for all vegetables in all cities"""
    
    cities = City.objects.all()
    vegetables = Vegetable.objects.all()
    
    if not cities.exists():
        print("❌ No cities found. Run populate_initial_data.py first.")
        return
    
    if not vegetables.exists():
        print("❌ No vegetables found. Run populate_initial_data.py first.")
        return
    
    # Clear existing predictions
    Prediction.objects.all().delete()
    print(f"🗑️  Cleared existing predictions")
    
    predictions_created = 0
    
    # Generate predictions for next 30 days
    for city in cities:
        for vegetable in vegetables:
            # Base price for this vegetable
            base_price = Decimal('50.00') if vegetable.name in ['Tomato', 'Onion', 'Potato'] else Decimal('80.00')
            
            # Generate predictions for next 30 days
            for days_ahead in range(1, 31):
                prediction_date = datetime.now().date() + timedelta(days=days_ahead)
                
                # Simulate price variation with some randomness
                price_variation = (days_ahead % 3) - 1  # -1, 0, or 1
                predicted_price = base_price + Decimal(str(price_variation * 5))
                
                # Calculate confidence (higher for nearer dates)
                confidence = max(0.5, 1.0 - (days_ahead / 30) * 0.4)
                
                # Calculate bounds
                lower_bound = predicted_price * Decimal('0.9')
                upper_bound = predicted_price * Decimal('1.1')
                
                # Choose model type based on days
                if days_ahead <= 7:
                    model_used = 'prophet'
                elif days_ahead <= 14:
                    model_used = 'arima'
                else:
                    model_used = 'ensemble'
                
                prediction = Prediction.objects.create(
                    vegetable=vegetable,
                    city=city,
                    predicted_price=predicted_price,
                    prediction_date=prediction_date,
                    model_used=model_used,
                    confidence=confidence,
                    lower_bound=lower_bound,
                    upper_bound=upper_bound
                )
                
                predictions_created += 1
    
    print(f"✅ Created {predictions_created} sample predictions")
    print(f"   - Cities: {cities.count()}")
    print(f"   - Vegetables: {vegetables.count()}")
    print(f"   - Days ahead: 30")
    print(f"   - Total: {cities.count()} × {vegetables.count()} × 30 = {predictions_created}")
    print(f"\n📊 Sample predictions for testing:")
    
    # Show sample
    sample_predictions = Prediction.objects.all()[:5]
    for pred in sample_predictions:
        print(f"   - {pred.vegetable.name} in {pred.city.name}: ₹{pred.predicted_price} on {pred.prediction_date} ({pred.model_used}, confidence: {pred.confidence:.2f})")

if __name__ == '__main__':
    print("🔄 Populating sample prediction data...\n")
    populate_predictions()
    print("\n✨ Done!")
