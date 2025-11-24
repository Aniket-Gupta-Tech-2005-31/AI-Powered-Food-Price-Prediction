import logging
import re
from decimal import Decimal

logger = logging.getLogger(__name__)


def clean_price_data(raw_prices):
    """
    Clean and validate price data before storing in database
    """
    cleaned = []

    for price in raw_prices:
        try:
            # Clean vegetable name
            vegetable_name = str(price.get('vegetable_name', '')).strip().title()
            if not vegetable_name:
                logger.warning(f"Skipping entry with no vegetable name: {price}")
                continue

            # Clean city name
            city_name = str(price.get('city_name', '')).strip().title()
            if not city_name:
                logger.warning(f"Skipping entry with no city name: {price}")
                continue

            # Clean and validate price
            try:
                price_per_kg = float(price.get('price_per_kg', 0))
                if price_per_kg <= 0:
                    logger.warning(f"Invalid price for {vegetable_name}: {price_per_kg}")
                    continue
            except (ValueError, TypeError):
                logger.warning(f"Could not parse price: {price.get('price_per_kg')}")
                continue

            # Clean source
            source = str(price.get('source', 'other')).lower().replace(' ', '_')
            valid_sources = ['bigbasket', 'jiomart', 'blinkit', 'local_market', 'government', 'other']
            if source not in valid_sources:
                source = 'other'

            # Clean location
            location = str(price.get('location', '')).strip()

            # Clean quality rating
            try:
                quality_rating = int(price.get('quality_rating', 5))
                quality_rating = max(1, min(5, quality_rating))
            except (ValueError, TypeError):
                quality_rating = 5

            cleaned.append({
                'vegetable_name': vegetable_name,
                'city_name': city_name,
                'price_per_kg': Decimal(str(price_per_kg)),
                'source': source,
                'location': location,
                'quality_rating': quality_rating
            })

        except Exception as e:
            logger.error(f"Error cleaning price entry {price}: {e}")
            continue

    logger.info(f"Cleaned {len(cleaned)} out of {len(raw_prices)} price entries")
    return cleaned


def remove_duplicates(prices):
    """
    Remove duplicate prices from the same source and time
    """
    unique_prices = {}

    for price in prices:
        key = (
            price['vegetable_name'],
            price['city_name'],
            price['source']
        )

        if key not in unique_prices:
            unique_prices[key] = price
        else:
            # Keep the one with higher quality rating
            if price['quality_rating'] > unique_prices[key]['quality_rating']:
                unique_prices[key] = price

    return list(unique_prices.values())


def validate_price_range(price, vegetable_name):
    """
    Validate if price is within reasonable range for the vegetable
    """
    # Realistic price ranges for common vegetables (in INR per kg)
    price_ranges = {
        'tomato': (20, 100),
        'onion': (20, 80),
        'potato': (15, 60),
        'spinach': (15, 50),
        'carrot': (20, 60),
        'cucumber': (20, 50),
        'capsicum': (40, 120),
        'broccoli': (60, 150),
        'cauliflower': (30, 80),
    }

    min_price, max_price = price_ranges.get(vegetable_name.lower(), (10, 200))

    if price < min_price or price > max_price:
        logger.warning(
            f"Price {price} for {vegetable_name} is outside normal range "
            f"({min_price}-{max_price})"
        )
        return False

    return True


def standardize_vegetable_names(prices):
    """
    Standardize vegetable names for consistency
    """
    name_mapping = {
        'tamato': 'Tomato',
        'tomatoe': 'Tomato',
        'tomatos': 'Tomato',
        'onoin': 'Onion',
        'potatoe': 'Potato',
        'potatos': 'Potato',
        'capsicum': 'Capsicum',
        'bell pepper': 'Capsicum',
        'leafy greens': 'Spinach',
        'greens': 'Spinach',
    }

    for price in prices:
        vegetable = price['vegetable_name'].lower()
        price['vegetable_name'] = name_mapping.get(vegetable, price['vegetable_name'])

    return prices
