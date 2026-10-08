"""
duckdb_loader.py
Loads transformed market data into a DuckDB database.
"""

import duckdb
import pandas as pd
import os
from finflow.utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_DB_PATH = "data/finflow.duckdb"


class DuckDBLoader:
    """Loads data into a local DuckDB database."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        """Create the market_data table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                date        TIMESTAMP,
                ticker      VARCHAR,
                open        DOUBLE,
                high        DOUBLE,
                low         DOUBLE,
                close       DOUBLE,
                volume      BIGINT,
                daily_return     DOUBLE,
                cumulative_return DOUBLE,
                sma_20      DOUBLE,
                sma_50      DOUBLE,
                volatility_30d DOUBLE,
                rsi_14      DOUBLE,
                loaded_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (date, ticker)
            )
        """)

    def load(self, df: pd.DataFrame) -> int:
        """Insert or replace records into market_data."""
        ticker = df["ticker"].iloc[0] if "ticker" in df.columns else "UNKNOWN"
        logger.info(f"Loading {len(df)} rows for {ticker} into DuckDB...")

        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO market_data
                SELECT
                    date, ticker, open, high, low, close, volume,
                    daily_return, cumulative_return,
                    sma_20, sma_50, volatility_30d, rsi_14,
                    CURRENT_TIMESTAMP
                FROM df
            """)

            count = self.conn.execute(
                "SELECT COUNT(*) FROM market_data WHERE ticker = ?", [ticker]
            ).fetchone()[0]

            logger.info(f"Load complete — {count} total rows for {ticker} in database")
            return count

        except Exception as e:
            logger.error(f"Load failed: {e}")
            raise

    def query(self, sql: str) -> pd.DataFrame:
        """Run a SQL query and return results as a DataFrame."""
        return self.conn.execute(sql).df()

    def close(self):
        self.conn.close()