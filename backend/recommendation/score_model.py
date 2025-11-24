import logging
from decimal import Decimal
from .rule_based import calculate_recommendation_score, get_recommendation_action

logger = logging.getLogger(__name__)


class ScoreBasedEngine:
    """
    Score-based recommendation engine that weighs multiple factors
    """

    def __init__(self):
        self.weights = {
            'price_change': 0.4,
            'trend': 0.25,
            'confidence': 0.2,
            'seasonality': 0.15,
        }

    def calculate_price_change_score(self, current_price, predicted_price):
        """
        Calculate score based on price change
        Negative score = buy now (prices going up)
        Positive score = wait (prices going down)
        """
        if current_price <= 0:
            return 0

        change_percent = (predicted_price - current_price) / current_price
        return change_percent

    def calculate_trend_score(self, historical_trend):
        """
        Calculate score based on historical trend
        """
        return historical_trend

    def calculate_confidence_boost(self, confidence):
        """
        Boost or reduce the score based on model confidence
        Higher confidence = stronger recommendation
        """
        if confidence < 0.5:
            return 0.5  # Low confidence, reduce impact
        else:
            return 1.0 + (confidence - 0.5)  # Higher confidence, boost impact

    def calculate_seasonality_score(self, vegetable_name, month):
        """
        Calculate score based on seasonal factors
        """
        seasonal_scores = {
            'Tomato': {
                1: -0.2, 2: -0.15, 3: -0.1, 4: 0, 5: 0.1, 6: 0.15,
                7: 0.2, 8: 0.15, 9: 0.1, 10: 0, 11: -0.1, 12: -0.15
            },
            'Onion': {
                1: 0.1, 2: 0.2, 3: 0.15, 4: 0.05, 5: 0, 6: -0.1,
                7: -0.15, 8: -0.1, 9: 0, 10: 0.1, 11: 0.15, 12: 0.2
            },
            'Potato': {
                1: 0.05, 2: 0.1, 3: 0.05, 4: 0, 5: -0.1, 6: -0.2,
                7: -0.25, 8: -0.2, 9: -0.1, 10: 0, 11: 0.1, 12: 0.15
            },
        }

        veg_scores = seasonal_scores.get(vegetable_name, {1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
                                                            6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                                                            11: 0, 12: 0})
        return veg_scores.get(month, 0)

    def generate_recommendation(self, current_price, predicted_price, trend,
                              confidence, vegetable_name, month):
        """
        Generate recommendation based on multiple factors
        """
        # Calculate component scores
        price_change_score = self.calculate_price_change_score(current_price, predicted_price)
        trend_score = self.calculate_trend_score(trend)
        confidence_boost = self.calculate_confidence_boost(confidence)
        seasonality_score = self.calculate_seasonality_score(vegetable_name, month)

        # Calculate weighted score
        final_score = (
            price_change_score * self.weights['price_change'] +
            trend_score * self.weights['trend'] +
            seasonality_score * self.weights['seasonality']
        ) * confidence_boost

        # Determine action
        if final_score > 0.15:
            action = 'Wait'
            reason = f'Predicted to drop by {abs(price_change_score)*100:.1f}%'
            potential_savings = abs(current_price - predicted_price)
        elif final_score < -0.15:
            action = 'Buy Now'
            reason = f'Price expected to rise or remain stable'
            potential_savings = 0
        else:
            action = 'Buy Now'
            reason = 'Price relatively stable, no strong trend'
            potential_savings = 0

        return {
            'action': action,
            'reason': reason,
            'score': final_score,
            'potential_savings': potential_savings,
            'confidence': confidence
        }


# Initialize default engine
score_engine = ScoreBasedEngine()
