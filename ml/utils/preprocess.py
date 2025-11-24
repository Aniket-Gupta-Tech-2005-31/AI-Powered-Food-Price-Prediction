import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import logging

logger = logging.getLogger(__name__)


def handle_missing_values(df, strategy='forward_fill'):
    """
    Handle missing values in price data
    """
    if strategy == 'forward_fill':
        df = df.fillna(method='ffill')
        df = df.fillna(method='bfill')
    elif strategy == 'mean':
        imputer = SimpleImputer(strategy='mean')
        df = pd.DataFrame(
            imputer.fit_transform(df),
            columns=df.columns
        )
    elif strategy == 'median':
        imputer = SimpleImputer(strategy='median')
        df = pd.DataFrame(
            imputer.fit_transform(df),
            columns=df.columns
        )

    return df


def normalize_prices(prices):
    """
    Normalize prices using StandardScaler
    """
    scaler = StandardScaler()
    normalized = scaler.fit_transform(prices.reshape(-1, 1))
    return normalized.flatten(), scaler


def denormalize_prices(normalized_prices, scaler):
    """
    Denormalize prices back to original scale
    """
    denormalized = scaler.inverse_transform(normalized_prices.reshape(-1, 1))
    return denormalized.flatten()


def add_features(df):
    """
    Add engineered features for model training
    """
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_month'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['week_of_year'] = df['date'].dt.isocalendar().week

    # Lag features
    df['price_lag_1'] = df['price'].shift(1)
    df['price_lag_7'] = df['price'].shift(7)
    df['price_lag_30'] = df['price'].shift(30)

    # Rolling statistics
    df['rolling_mean_7'] = df['price'].rolling(window=7).mean()
    df['rolling_mean_30'] = df['price'].rolling(window=30).mean()
    df['rolling_std_7'] = df['price'].rolling(window=7).std()

    return df


def create_train_test_split(df, test_size=0.2):
    """
    Create train-test split maintaining temporal order
    """
    split_idx = int(len(df) * (1 - test_size))

    train = df[:split_idx]
    test = df[split_idx:]

    return train, test


def detect_outliers(df, column='price', threshold=3):
    """
    Detect outliers using z-score method
    """
    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
    outliers = z_scores > threshold

    logger.info(f"Detected {outliers.sum()} outliers")
    return outliers


def remove_outliers(df, column='price', threshold=3):
    """
    Remove outliers from dataframe
    """
    outliers = detect_outliers(df, column, threshold)
    df_clean = df[~outliers].copy()

    logger.info(f"Removed {len(df) - len(df_clean)} outlier records")
    return df_clean


class DataPreprocessor:
    """
    Main data preprocessing class
    """

    def __init__(self):
        self.scaler = None
        self.feature_columns = None

    def preprocess(self, df, remove_outliers=True):
        """
        Complete preprocessing pipeline
        """
        try:
            # Sort by date
            df = df.sort_values('date').reset_index(drop=True)

            # Handle missing values
            df = handle_missing_values(df)

            # Remove outliers if requested
            if remove_outliers:
                df = remove_outliers(df)

            # Add features
            df = add_features(df)

            # Handle any NaN values from feature engineering
            df = handle_missing_values(df)

            logger.info("Data preprocessing completed successfully")
            return df

        except Exception as e:
            logger.error(f"Error during preprocessing: {e}")
            return df
