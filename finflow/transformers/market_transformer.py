"""
market_transformer.py
Transforms raw market data — calculates returns, volatility, and moving averages.
"""

import pandas as pd
import numpy as np
from finflow.utils.logger import get_logger

logger = get_logger(__name__)


class MarketDataTransformer:
    """Transforms raw OHLCV data into enriched analytical data."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def transform(self) -> pd.DataFrame:
        """Run the full transformation pipeline."""
        if self.df.empty:
            raise ValueError("Cannot transform empty DataFrame")

        logger.info("Transforming data...")
        self._clean()
        self._calculate_returns()
        self._calculate_moving_averages()
        self._calculate_volatility()
        self._calculate_rsi()

        logger.info(f"Transformation complete — {len(self.df)} rows, {len(self.df.columns)} columns")
        return self.df

    def _clean(self):
        """Drop nulls and ensure correct types."""
        self.df.dropna(subset=["close"], inplace=True)
        self.df["date"] = pd.to_datetime(self.df["date"]).dt.tz_localize(None)
        self.df.sort_values("date", inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def _calculate_returns(self):
        """Calculate daily and cumulative returns."""
        self.df["daily_return"] = self.df["close"].pct_change()
        self.df["cumulative_return"] = (1 + self.df["daily_return"]).cumprod() - 1

    def _calculate_moving_averages(self):
        """Calculate 20-day and 50-day simple moving averages."""
        self.df["sma_20"] = self.df["close"].rolling(window=20).mean()
        self.df["sma_50"] = self.df["close"].rolling(window=50).mean()

    def _calculate_volatility(self):
        """Calculate 30-day rolling annualised volatility."""
        self.df["volatility_30d"] = (
            self.df["daily_return"].rolling(window=30).std() * np.sqrt(252)
        )

    def _calculate_rsi(self, period: int = 14):
        """Calculate the Relative Strength Index (RSI)."""
        delta = self.df["close"].diff()
        gain = delta.clip(lower=0).rolling(window=period).mean()
        loss = (-delta.clip(upper=0)).rolling(window=period).mean()
        rs = gain / loss
        self.df["rsi_14"] = 100 - (100 / (1 + rs))