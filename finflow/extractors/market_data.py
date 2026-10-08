"""
market_data.py
Extracts historical market data from Yahoo Finance.
"""

import yfinance as yf
import pandas as pd
from finflow.utils.logger import get_logger

logger = get_logger(__name__)


class MarketDataExtractor:
    """Extracts stock market data using yfinance."""

    VALID_PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]

    def __init__(self, ticker: str, period: str = "1y"):
        if period not in self.VALID_PERIODS:
            raise ValueError(f"Invalid period '{period}'. Choose from: {self.VALID_PERIODS}")
        self.ticker = ticker.upper()
        self.period = period

    def extract(self) -> pd.DataFrame:
        """Download historical OHLCV data for the ticker."""
        logger.info(f"Extracting data for {self.ticker} ({self.period})...")

        try:
            ticker_obj = yf.Ticker(self.ticker)
            df = ticker_obj.history(period=self.period)

            if df.empty:
                raise ValueError(f"No data found for ticker '{self.ticker}'. Check if it's valid.")

            df = df.reset_index()
            df.columns = [c.lower().replace(" ", "_") for c in df.columns]
            df["ticker"] = self.ticker

            logger.info(f"Extracted {len(df)} rows for {self.ticker}")
            return df

        except Exception as e:
            logger.error(f"Extraction failed for {self.ticker}: {e}")
            raise