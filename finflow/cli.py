"""
cli.py
Command-line interface for FinFlow.
"""

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from finflow.pipeline import FinFlowPipeline
from finflow.loaders import DuckDBLoader

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="FinFlow")
def cli():
    """FinFlow — Financial ETL Pipeline CLI.

    Extract, transform and load market data from Yahoo Finance into DuckDB.
    """
    pass


@cli.command()
@click.option("--ticker", "-t", required=True, help="Stock ticker symbol (e.g. AAPL, NPN.JO)")
@click.option("--period", "-p", default="1y", show_default=True,
              help="Data period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y")
@click.option("--db", default="data/finflow.duckdb", show_default=True,
              help="Path to DuckDB database file")
def run(ticker: str, period: str, db: str):
    """Run the ETL pipeline for a stock ticker."""
    try:
        pipeline = FinFlowPipeline(ticker=ticker, period=period, db_path=db)
        result = pipeline.run()

        table = Table(title="Pipeline Results", style="green")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Ticker", result["ticker"])
        table.add_row("Period", result["period"])
        table.add_row("Rows Extracted", str(result["rows_extracted"]))
        table.add_row("Rows in Database", str(result["rows_loaded"]))

        console.print(table)

    except ValueError as e:
        rprint(f"[red]Error:[/red] {e}")
        raise SystemExit(1)
    except Exception as e:
        rprint(f"[red]Unexpected error:[/red] {e}")
        raise SystemExit(1)


@cli.command()
@click.option("--ticker", "-t", required=True, help="Stock ticker symbol")
@click.option("--db", default="data/finflow.duckdb", show_default=True,
              help="Path to DuckDB database file")
@click.option("--rows", "-n", default=10, show_default=True, help="Number of rows to show")
def show(ticker: str, db: str, rows: int):
    """Show recent data for a ticker from the database."""
    try:
        loader = DuckDBLoader(db)
        df = loader.query(f"""
            SELECT date, ticker, close, daily_return, sma_20, sma_50, rsi_14
            FROM market_data
            WHERE ticker = '{ticker.upper()}'
            ORDER BY date DESC
            LIMIT {rows}
        """)
        loader.close()

        if df.empty:
            rprint(f"[yellow]No data found for {ticker.upper()}. Run 'finflow run --ticker {ticker}' first.[/yellow]")
            return

        table = Table(title=f"{ticker.upper()} — Recent Data", style="blue")
        for col in df.columns:
            table.add_column(col, style="white")
        for _, row in df.iterrows():
            table.add_row(*[str(round(v, 4)) if isinstance(v, float) else str(v) for v in row])

        console.print(table)

    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise SystemExit(1)


@cli.command()
@click.option("--db", default="data/finflow.duckdb", show_default=True,
              help="Path to DuckDB database file")
def tickers(db: str):
    """List all tickers currently stored in the database."""
    try:
        loader = DuckDBLoader(db)
        df = loader.query("""
            SELECT ticker,
                   COUNT(*) as rows,
                   MIN(date) as from_date,
                   MAX(date) as to_date
            FROM market_data
            GROUP BY ticker
            ORDER BY ticker
        """)
        loader.close()

        if df.empty:
            rprint("[yellow]No tickers in database yet. Run 'finflow run' to add some.[/yellow]")
            return

        table = Table(title="Stored Tickers", style="cyan")
        for col in df.columns:
            table.add_column(col, style="white")
        for _, row in df.iterrows():
            table.add_row(*[str(v) for v in row])

        console.print(table)

    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise SystemExit(1)