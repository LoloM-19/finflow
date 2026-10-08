"""
logger.py
Structured logging utility for FinFlow.
"""

import logging
from rich.logging import RichHandler


def get_logger(name: str) -> logging.Logger:
    """Get a logger with rich formatting."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger(name)