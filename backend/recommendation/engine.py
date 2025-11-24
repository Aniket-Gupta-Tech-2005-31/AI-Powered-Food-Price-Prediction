import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Main recommendation engine that orchestrates rule-based and score-based engines
    """

    def __init__(self, rule_engine=None, score_engine=None):
        self.rule_engine = rule_engine
        self.score_engine = score_engine

    def generate_recommendation(self, current_price, predicted_price, trend,
                              confidence, vegetable_name, month):
        """
        Generate buy/wait recommendation using ensemble approach
        """
        try:
            if self.score_engine:
                recommendation = self.score_engine.generate_recommendation(
                    current_price=current_price,
                    predicted_price=predicted_price,
                    trend=trend,
                    confidence=confidence,
                    vegetable_name=vegetable_name,
                    month=month
                )
                return recommendation
            else:
                logger.warning("No scoring engine available")
                return self._default_recommendation(current_price, predicted_price)

        except Exception as e:
            logger.error(f"Error generating recommendation: {e}")
            return self._default_recommendation(current_price, predicted_price)

    def _default_recommendation(self, current_price, predicted_price):
        """Default recommendation when engines fail"""
        if predicted_price < current_price * 0.95:
            action = 'Wait'
            reason = 'Expected price reduction'
            savings = current_price - predicted_price
        else:
            action = 'Buy Now'
            reason = 'Price likely to increase or stay same'
            savings = 0

        return {
            'action': action,
            'reason': reason,
            'potential_savings': savings,
            'confidence': 0.5
        }
