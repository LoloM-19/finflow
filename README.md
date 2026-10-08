# FinFlow — Financial ETL Pipeline CLI

A production-grade command-line ETL pipeline that extracts financial market data, transforms it with technical indicators, and loads it into a DuckDB database.

## Features
- Extract historical OHLCV data for any stock ticker via yfinance
- Transform: daily returns, cumulative returns, SMA-20, SMA-50, 30-day volatility, RSI-14
- Load into a local DuckDB database with full schema
- Clean CLI interface with `run`, `show`, and `tickers` commands
- Structured logging with Rich
- 12 unit tests with pytest
- GitHub Actions CI — tests run on every push

## Tech Stack
Python | yfinance | pandas | DuckDB | Click | Rich | pytest | GitHub Actions

## Installation

```bash
git clone https://github.com/LoloM-19/finflow.git
cd finflow
pip install -r requirements.txt
pip install -e .
```

## Usage

### Run the pipeline
```bash
finflow run --ticker NPN.JO --period 1y
finflow run --ticker AAPL --period 6mo
```

### View recent data
```bash
finflow show --ticker NPN.JO --rows 10
```

### List all stored tickers
```bash
finflow tickers
```

### Get help
```bash
finflow --help
finflow run --help
```

## Project Structure
finflow/
├── finflow/
│ ├── extractors/ # Yahoo Finance data extraction
│ ├── transformers/ # Returns, moving averages, RSI
│ ├── loaders/ # DuckDB loader
│ ├── utils/ # Structured logging
│ ├── cli.py # Click CLI commands
│ └── pipeline.py # ETL orchestrator
├── tests/
│ ├── test_transformers.py
│ └── test_pipeline.py
├── .github/workflows/ci.yml
├── requirements.txt
└── setup.py


## CI/CD
GitHub Actions runs the full test suite on every push to `main`.

## JSE Tickers
South African stocks use the `.JO` suffix:
- `NPN.JO` — Naspers
- `SBK.JO` — Standard Bank
- `FSR.JO` — FirstRand
- `MTN.JO` — MTN Group
- `AGL.JO` — Anglo American