import logging

logger = logging.getLogger(__name__)


def save_to_db(prices, model):
    """
    Save prices to database using Django ORM
    """
    try:
        count = 0
        for price_data in prices:
            try:
                obj = model.objects.create(**price_data)
                count += 1
            except Exception as e:
                logger.error(f"Error saving price: {e}")
                continue

        logger.info(f"Successfully saved {count} price entries")
        return count

    except Exception as e:
        logger.error(f"Error in save_to_db: {e}")
        return 0
