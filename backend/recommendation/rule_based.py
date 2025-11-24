import logging

logger = logging.getLogger(__name__)


def calculate_recommendation_score(current_price, predicted_price, trend, season_factor=1.0):
    """
    Calculate a score to determine buy/wait recommendation.
    Higher score = better to wait
    Lower score = better to buy now
    """
    # Price drop factor (0 to 1)
    if current_price > 0:
        price_change = (predicted_price - current_price) / current_price
        price_drop = max(-1, min(1, price_change))
    else:
        price_drop = 0

    # Trend factor (already normalized -1 to 1)
    trend_factor = trend

    # Score calculation
    score = (trend_factor * 0.4 + price_drop * 0.6) * season_factor

    return score


def get_recommendation_action(score, confidence=0.5):
    """
    Determine buy/wait action based on score and confidence
    """
    # If score > 0.1 and confidence > 0.6, recommend wait
    if score > 0.1 and confidence > 0.6:
        action = 'Wait'
        reason = 'Price likely to drop. Waiting could save money.'
    # If score < -0.1 and confidence > 0.6, recommend buy now
    elif score < -0.1 and confidence > 0.6:
        action = 'Buy Now'
        reason = 'Price likely to increase. Buy while rates are low.'
    else:
        action = 'Buy Now'
        reason = 'Price relatively stable. Confidence is low for significant change.'

    return action, reason


def get_seasonal_factor(vegetable_name, current_month):
    """
    Get seasonal factor for vegetable
    Affects how much to adjust recommendations
    """
    seasonal_data = {
        'Tomato': {
            'peak_season': [5, 6, 7, 8, 9],  # May to September
            'off_season': [11, 12, 1, 2, 3],  # Nov to March
        },
        'Onion': {
            'peak_season': [2, 3, 4],  # Feb to April
            'off_season': [8, 9, 10, 11],  # Aug to Nov
        },
        'Potato': {
            'peak_season': [1, 2, 3, 4],  # Jan to April
            'off_season': [8, 9, 10],  # Aug to Oct
        },
    }

    veg_data = seasonal_data.get(vegetable_name, {})
    peak_season = veg_data.get('peak_season', [])
    off_season = veg_data.get('off_season', [])

    if current_month in peak_season:
        return 0.8  # Prices lower in peak season
    elif current_month in off_season:
        return 1.3  # Prices higher in off season
    else:
        return 1.0  # Normal


class RuleBasedRecommendationEngine:
    """
    Rule-based recommendation engine for buy/wait decisions
    """

    def __init__(self):
        self.rules = []

    def add_rule(self, condition, action, reason):
        """Add a rule to the engine"""
        self.rules.append({
            'condition': condition,
            'action': action,
            'reason': reason
        })

    def evaluate(self, current_price, predicted_price, trend, vegetable_name):
        """
        Evaluate rules and return recommendation
        """
        for rule in self.rules:
            if rule['condition'](current_price, predicted_price, trend):
                return {
                    'action': rule['action'],
                    'reason': rule['reason']
                }

        # Default recommendation
        return {
            'action': 'Buy Now',
            'reason': 'No specific rule matched'
        }

    def setup_default_rules(self):
        """Setup default recommendation rules"""
        # Rule 1: If price dropping significantly
        self.add_rule(
            condition=lambda cp, pp, t: (cp - pp) > cp * 0.15,
            action='Wait',
            reason='Significant price drop expected'
        )

        # Rule 2: If price increasing
        self.add_rule(
            condition=lambda cp, pp, t: pp > cp * 1.1,
            action='Buy Now',
            reason='Price increase expected'
        )

        # Rule 3: If trend is strongly negative
        self.add_rule(
            condition=lambda cp, pp, t: t < -0.3,
            action='Wait',
            reason='Strong downward trend detected'
        )

        # Rule 4: If trend is strongly positive
        self.add_rule(
            condition=lambda cp, pp, t: t > 0.3,
            action='Buy Now',
            reason='Strong upward trend detected'
        )


# Initialize default engine
default_engine = RuleBasedRecommendationEngine()
default_engine.setup_default_rules()
