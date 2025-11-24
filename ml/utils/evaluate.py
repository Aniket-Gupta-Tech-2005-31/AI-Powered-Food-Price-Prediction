import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import logging

logger = logging.getLogger(__name__)


def calculate_mae(y_true, y_pred):
    """Calculate Mean Absolute Error"""
    return mean_absolute_error(y_true, y_pred)


def calculate_rmse(y_true, y_pred):
    """Calculate Root Mean Squared Error"""
    return np.sqrt(mean_squared_error(y_true, y_pred))


def calculate_mape(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error"""
    # Avoid division by zero
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def calculate_r2(y_true, y_pred):
    """Calculate R-squared score"""
    return r2_score(y_true, y_pred)


def evaluate_model(y_true, y_pred, model_name='Model'):
    """
    Evaluate model performance with multiple metrics
    """
    mae = calculate_mae(y_true, y_pred)
    rmse = calculate_rmse(y_true, y_pred)
    mape = calculate_mape(y_true, y_pred)
    r2 = calculate_r2(y_true, y_pred)

    metrics = {
        'model': model_name,
        'mae': mae,
        'rmse': rmse,
        'mape': mape,
        'r2': r2
    }

    logger.info(f"\n{model_name} Evaluation Metrics:")
    logger.info(f"  MAE:  {mae:.4f}")
    logger.info(f"  RMSE: {rmse:.4f}")
    logger.info(f"  MAPE: {mape:.2f}%")
    logger.info(f"  R2:   {r2:.4f}")

    return metrics


def compare_models(model_results):
    """
    Compare multiple model results
    """
    results_df = pd.DataFrame(model_results)
    logger.info("\nModel Comparison:")
    logger.info(results_df.to_string())

    # Find best model by each metric
    best_by_mae = results_df.loc[results_df['mae'].idxmin()]
    best_by_rmse = results_df.loc[results_df['rmse'].idxmin()]
    best_by_r2 = results_df.loc[results_df['r2'].idxmax()]

    logger.info(f"\nBest by MAE: {best_by_mae['model']}")
    logger.info(f"Best by RMSE: {best_by_rmse['model']}")
    logger.info(f"Best by R2: {best_by_r2['model']}")

    return results_df


class ModelEvaluator:
    """
    Comprehensive model evaluation class
    """

    def __init__(self):
        self.results = []

    def evaluate(self, y_true, y_pred, model_name):
        """Evaluate a model and store results"""
        metrics = evaluate_model(y_true, y_pred, model_name)
        self.results.append(metrics)
        return metrics

    def get_best_model(self, metric='rmse'):
        """Get best model by specified metric"""
        if not self.results:
            return None

        if metric == 'mae':
            best = min(self.results, key=lambda x: x['mae'])
        elif metric == 'rmse':
            best = min(self.results, key=lambda x: x['rmse'])
        elif metric == 'r2':
            best = max(self.results, key=lambda x: x['r2'])
        else:
            best = min(self.results, key=lambda x: x['mape'])

        return best

    def get_summary(self):
        """Get summary of all evaluations"""
        if not self.results:
            return None

        summary = {
            'total_models': len(self.results),
            'best_by_mae': self.get_best_model('mae'),
            'best_by_rmse': self.get_best_model('rmse'),
            'best_by_r2': self.get_best_model('r2'),
        }

        return summary


# Import pandas for comparison
import pandas as pd
