from scraper.gov_api_fetch import fetch_government_prices, fetch_alternative_government_data
from scraper.online_store_scraper import fetch_online_store_prices
from scraper.clean_data import clean_price_data
import logging

logger = logging.getLogger(__name__)


def fetch_all_prices():
    """
    Master function to fetch prices from all sources
    """
    try:
        all_prices = []

        # Fetch from government API
        logger.info("Fetching government prices...")
        gov_prices = fetch_government_prices()
        if not gov_prices:
            logger.warning("Government API failed, trying alternative...")
            gov_prices = fetch_alternative_government_data()
        all_prices.extend(gov_prices)

        # Fetch from online stores
        logger.info("Fetching online store prices...")
        online_prices = fetch_online_store_prices()
        all_prices.extend(online_prices)

        logger.info(f"Total raw prices fetched: {len(all_prices)}")
        return all_prices

    except Exception as e:
        logger.error(f"Error in fetch_all_prices: {e}")
        return []


def fetch_and_process_prices():
    """
    Fetch and clean prices in one go
    """
    try:
        raw_prices = fetch_all_prices()
        cleaned_prices = clean_price_data(raw_prices)
        logger.info(f"Successfully processed {len(cleaned_prices)} prices")
        return cleaned_prices

    except Exception as e:
        logger.error(f"Error in fetch_and_process_prices: {e}")
        return []
