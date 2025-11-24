import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def fetch_government_prices():
    """
    Fetch prices from Government Agmarknet API (Tomato, Onion, Potato)
    https://agmarknet.gov.in/
    """
    try:
        prices = []

        # Agmarknet API endpoint
        url = "https://api.agmarknet.gov.in/api/datapoints"

        # Parameters for API
        params = {
            'commodityId': '1',  # Example: Tomato
            'stateId': 'DL',
            'districtId': 'D1',
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if 'response' in data:
            for entry in data['response']:
                prices.append({
                    'vegetable_name': entry.get('commodity', 'Unknown'),
                    'city_name': entry.get('state', 'Unknown'),
                    'price_per_kg': float(entry.get('priceCurrent', 0)) / 100,
                    'source': 'government',
                    'location': entry.get('market', 'Government'),
                    'quality_rating': 5
                })

        logger.info(f"Successfully fetched {len(prices)} prices from government API")
        return prices

    except Exception as e:
        logger.error(f"Error fetching government prices: {e}")
        return []


def fetch_alternative_government_data():
    """
    Fallback method to fetch from OGD (Open Government Data) portal
    """
    try:
        prices = []

        # Sample data for demonstration
        sample_data = [
            {
                'vegetable_name': 'Tomato',
                'city_name': 'Delhi',
                'price_per_kg': 45.50,
                'source': 'government',
                'location': 'Azadpur Market',
                'quality_rating': 5
            },
            {
                'vegetable_name': 'Onion',
                'city_name': 'Delhi',
                'price_per_kg': 38.00,
                'source': 'government',
                'location': 'Azadpur Market',
                'quality_rating': 5
            },
            {
                'vegetable_name': 'Potato',
                'city_name': 'Mumbai',
                'price_per_kg': 32.75,
                'source': 'government',
                'location': 'APMC Market',
                'quality_rating': 5
            },
        ]

        logger.info(f"Using sample government data: {len(sample_data)} entries")
        return sample_data

    except Exception as e:
        logger.error(f"Error fetching alternative government data: {e}")
        return []
