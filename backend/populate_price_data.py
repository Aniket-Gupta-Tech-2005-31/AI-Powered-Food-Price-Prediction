"""
Script to populate realistic sample price data for the last 60 days
This creates daily price entries from different sources with realistic variations
"""
import os
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import City, Vegetable, PriceEntry

def populate_price_data():
    """Add realistic price data for last 60 days"""
    
    cities = City.objects.all()
    vegetables = Vegetable.objects.all()
    
    if not cities.exists():
        print("❌ No cities found. Run populate_initial_data.py first.")
        return
    
    if not vegetables.exists():
        print("❌ No vegetables found. Run populate_initial_data.py first.")
        return
    
    # Clear existing price entries
    PriceEntry.objects.all().delete()
    print(f"🗑️  Cleared existing price entries\n")
    
    # Base prices for vegetables (in rupees per kg)
    base_prices = {
        'Tomato': 40,
        'Onion': 45,
        'Potato': 25,
        'Spinach': 30,
        'Carrot': 35,
        'Cabbage': 20,
        'Broccoli': 60,
        'Bell Pepper': 80,
        'Garlic': 120,
        'Ginger': 100,
        'Cucumber': 25,
        'Bitter Gourd': 50,
        'Ridge Gourd': 30,
        'Bottle Gourd': 28,
        'Cauliflower': 45,
    }
    
    # Online sources with price markup/discount
    sources = {
        'bigbasket': 1.15,    # 15% premium (delivery, packaging)
        'jiomart': 1.10,      # 10% premium
        'blinkit': 1.20,      # 20% premium (faster delivery)
        'agmarknet': 1.0,     # Base market price (government data)
        'local': 0.95,        # 5% cheaper (no middleman)
    }
    
    # Locations for local markets
    locations = ['Central Market', 'Wholesale Center', 'Retail Store', 'Street Vendor', 'Supermarket']
    
    # Quality ratings
    quality_choices = [1, 2, 3, 4]
    
    prices_created = 0
    start_date = datetime.now().date() - timedelta(days=60)
    
    print("📊 Generating price data...\n")
    
    # Generate prices for last 60 days
    for day_offset in range(60):
        current_date = start_date + timedelta(days=day_offset)
        
        for city in cities:
            for vegetable in vegetables:
                base_price = Decimal(str(base_prices.get(vegetable.name, 50)))
                
                # Add daily seasonal variation (prices change slightly each day)
                day_variation = Decimal(str(random.uniform(-5, 5)))
                
                # Add weekly pattern (weekend prices higher)
                weekday = current_date.weekday()
                weekend_markup = Decimal(str(2 if weekday >= 4 else 0))  # Friday onwards
                
                for source, multiplier in sources.items():
                    # Calculate source-specific price
                    source_price = (base_price + day_variation + weekend_markup) * Decimal(str(multiplier))
                    
                    # Add small random noise for realism
                    noise = Decimal(str(random.uniform(-2, 2)))
                    final_price = source_price + noise
                    
                    # Ensure price is positive and reasonable
                    if final_price < 5:
                        final_price = Decimal('5.00')
                    
                    # Choose quality based on source
                    if source == 'blinkit':
                        quality = random.choice([3, 4])  # Better quality
                    elif source == 'local':
                        quality = random.choice([1, 2, 3])  # Variable quality
                    else:
                        quality = random.choice([2, 3, 4])  # Good quality
                    
                    # Choose location
                    location = random.choice(locations) if source == 'local' else source.title()
                    
                    # Create price entry with timestamp in the morning
                    timestamp = datetime.combine(
                        current_date,
                        datetime.min.time().replace(hour=random.randint(6, 10))
                    )
                    
                    PriceEntry.objects.create(
                        vegetable=vegetable,
                        city=city,
                        price_per_kg=final_price,
                        source=source,
                        location=location,
                        quality_rating=quality,
                        timestamp=timestamp
                    )
                    
                    prices_created += 1
    
    print(f"✅ Created {prices_created} price entries")
    print(f"   - Time period: Last 60 days")
    print(f"   - Cities: {cities.count()}")
    print(f"   - Vegetables: {vegetables.count()}")
    print(f"   - Sources: {len(sources)}")
    print(f"   - Total: 60 days × {cities.count()} cities × {vegetables.count()} vegetables × {len(sources)} sources")
    
    print(f"\n📈 Sample prices (most recent):")
    sample = PriceEntry.objects.order_by('-timestamp')[:10]
    for entry in sample:
        print(f"   - {entry.vegetable.name} in {entry.city.name}: ₹{entry.price_per_kg:.2f} ({entry.source}, {entry.get_quality_rating_display()})")
    
    print(f"\n💰 Price range samples:")
    for vegetable in vegetables[:5]:
        entries = PriceEntry.objects.filter(vegetable=vegetable)
        if entries.exists():
            min_price = min(e.price_per_kg for e in entries)
            max_price = max(e.price_per_kg for e in entries)
            avg_price = sum(e.price_per_kg for e in entries) / len(entries)
            print(f"   - {vegetable.name}: ₹{min_price:.2f} - ₹{max_price:.2f} (avg: ₹{avg_price:.2f})")

if __name__ == '__main__':
    print("=" * 60)
    print("🔄 Populating realistic price data...")
    print("=" * 60 + "\n")
    populate_price_data()
    print("\n✨ Price data population complete!")
    print("=" * 60)
