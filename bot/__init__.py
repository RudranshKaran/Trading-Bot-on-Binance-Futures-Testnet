"""
Binance Futures Testnet Trading Bot - Core Backend Module

This package contains the core business logic for order execution,
validation, API communication, and logging configuration.
"""

from bot.logging_config import get_logger
from bot.client import BinanceTestnetClient, ConfigurationError

__all__ = [
    "get_logger",
    "BinanceTestnetClient",
    "ConfigurationError",
]
