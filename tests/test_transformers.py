"""
test_transformers.py
Unit tests for the MarketDataTransformer.
"""

import pytest
import pandas as pd
import numpy as np
from finflow.transformers import MarketDataTransformer


def make_sample_df(rows: int = 100) -> pd.DataFrame:
    """Create a sample OHLCV DataFrame for testing."""
    dates = pd.date_range(start="2024-01-01", periods=rows, freq="B")
    close = 100 + np.cumsum(np.random.randn(rows))
    return pd.DataFrame({
        "date": dates,
        "ticker": "TEST",
        "open": close * 0.99,
        "high": close * 1.02,
        "low": close * 0.98,
        "close": close,
        "volume": np.random.randint(1000000, 5000000, rows),
    })


def test_transform_returns_dataframe():
    df = make_sample_df()
    transformer = MarketDataTransformer(df)
    result = transformer.transform()
    assert isinstance(result, pd.DataFrame)


def test_transform_adds_daily_return():
    df = make_sample_df()
    result = MarketDataTransformer(df).transform()
    assert "daily_return" in result.columns


def test_transform_adds_cumulative_return():
    df = make_sample_df()
    result = MarketDataTransformer(df).transform()
    assert "cumulative_return" in result.columns


def test_transform_adds_moving_averages():
    df = make_sample_df()
    result = MarketDataTransformer(df).transform()
    assert "sma_20" in result.columns
    assert "sma_50" in result.columns


def test_transform_adds_volatility():
    df = make_sample_df()
    result = MarketDataTransformer(df).transform()
    assert "volatility_30d" in result.columns


def test_transform_adds_rsi():
    df = make_sample_df()
    result = MarketDataTransformer(df).transform()
    assert "rsi_14" in result.columns


def test_rsi_values_within_range():
    df = make_sample_df(rows=100)
    result = MarketDataTransformer(df).transform()
    rsi = result["rsi_14"].dropna()
    assert (rsi >= 0).all() and (rsi <= 100).all()


def test_transform_sorts_by_date():
    df = make_sample_df()
    df = df.sample(frac=1).reset_index(drop=True)
    result = MarketDataTransformer(df).transform()
    assert result["date"].is_monotonic_increasing


def test_empty_dataframe_raises():
    df = pd.DataFrame(columns=["date", "ticker", "open", "high", "low", "close", "volume"])
    with pytest.raises(Exception):
        MarketDataTransformer(df).transform()