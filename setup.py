from setuptools import setup, find_packages

setup(
    name="finflow",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "yfinance>=0.2.0",
        "pandas>=2.0.0",
        "duckdb>=0.10.0",
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "finflow=finflow.cli:cli",
        ],
    },
    author="Lolo Mphahlele",
    author_email="lolomphahlele6@gmail.com",
    description="A command-line financial ETL pipeline",
    python_requires=">=3.9",
)