"""
pipeline.py
Orchestrates the full ETL pipeline: Extract → Transform → Load.
"""

from finflow.extractors import MarketDataExtractor
from finflow.transformers import MarketDataTransformer
from finflow.loaders import DuckDBLoader
from finflow.utils.logger import get_logger

logger = get_logger(__name__)


class FinFlowPipeline:
    """Orchestrates the Extract → Transform → Load pipeline."""

    def __init__(self, ticker: str, period: str = "1y", db_path: str = "data/finflow.duckdb"):
        self.ticker = ticker
        self.period = period
        self.db_path = db_path

    def run(self) -> dict:
        """Execute the full ETL pipeline."""
        logger.info(f"Starting FinFlow pipeline for {self.ticker}")

        # Extract
        extractor = MarketDataExtractor(self.ticker, self.period)
        raw_df = extractor.extract()

        # Transform
        transformer = MarketDataTransformer(raw_df)
        transformed_df = transformer.transform()

        # Load
        loader = DuckDBLoader(self.db_path)
        count = loader.load(transformed_df)
        loader.close()

        result = {
            "ticker": self.ticker,
            "period": self.period,
            "rows_extracted": len(raw_df),
            "rows_loaded": count,
            "columns": list(transformed_df.columns),
        }

        logger.info(f"Pipeline complete for {self.ticker}")
        return result