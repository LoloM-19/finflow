"""
test_pipeline.py
Unit tests for the FinFlowPipeline.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from finflow.pipeline import FinFlowPipeline


def make_mock_df(rows: int = 60) -> pd.DataFrame:
    """Create a mock extracted DataFrame."""
    dates = pd.date_range(start="2024-01-01", periods=rows, freq="B")
    close = 100 + np.cumsum(np.random.randn(rows))
    return pd.DataFrame({
        "date": dates,
        "ticker": "MOCK",
        "open": close * 0.99,
        "high": close * 1.02,
        "low": close * 0.98,
        "close": close,
        "volume": np.random.randint(1000000, 5000000, rows),
    })


@patch("finflow.pipeline.DuckDBLoader")
@patch("finflow.pipeline.MarketDataExtractor")
def test_pipeline_run_returns_dict(mock_extractor, mock_loader):
    mock_extractor.return_value.extract.return_value = make_mock_df()
    mock_loader.return_value.load.return_value = 60
    mock_loader.return_value.close.return_value = None

    pipeline = FinFlowPipeline(ticker="MOCK", period="1y")
    result = pipeline.run()

    assert isinstance(result, dict)
    assert result["ticker"] == "MOCK"
    assert result["rows_extracted"] == 60


@patch("finflow.pipeline.DuckDBLoader")
@patch("finflow.pipeline.MarketDataExtractor")
def test_pipeline_result_has_required_keys(mock_extractor, mock_loader):
    mock_extractor.return_value.extract.return_value = make_mock_df()
    mock_loader.return_value.load.return_value = 60
    mock_loader.return_value.close.return_value = None

    pipeline = FinFlowPipeline(ticker="MOCK", period="1y")
    result = pipeline.run()

    assert "ticker" in result
    assert "period" in result
    assert "rows_extracted" in result
    assert "rows_loaded" in result
    assert "columns" in result


@patch("finflow.pipeline.DuckDBLoader")
@patch("finflow.pipeline.MarketDataExtractor")
def test_pipeline_calls_extractor(mock_extractor, mock_loader):
    mock_extractor.return_value.extract.return_value = make_mock_df()
    mock_loader.return_value.load.return_value = 60
    mock_loader.return_value.close.return_value = None

    pipeline = FinFlowPipeline(ticker="MOCK", period="6mo")
    pipeline.run()

    mock_extractor.assert_called_once_with("MOCK", "6mo")
    mock_extractor.return_value.extract.assert_called_once()