"""
Centralized Logging Configuration

This module provides a unified logging setup for the Binance Futures Testnet Trading Bot.
All backend modules should import and use the logger from this module to ensure
consistent logging behavior across the application.
"""

import logging
import os
from pathlib import Path


# Log file configuration
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "trading_bot.log"

# Log format: Timestamp | Level | Message
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Logger name used across the application
LOGGER_NAME = "trading_bot"

# Module-level logger instance (initialized lazily)
_logger = None


def _ensure_log_directory() -> None:
    """Create the log directory if it does not exist."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def _configure_logger() -> logging.Logger:
    """
    Configure and return the application logger.
    
    Returns:
        logging.Logger: Configured logger instance with file handler.
    """
    _ensure_log_directory()
    
    logger = logging.getLogger(LOGGER_NAME)
    
    # Avoid adding duplicate handlers if already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # File handler - logs to trading_bot.log
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    
    logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger() -> logging.Logger:
    """
    Get the centralized application logger.
    
    This function returns a singleton logger instance that is shared
    across all backend modules. The logger writes to logs/trading_bot.log.
    
    Returns:
        logging.Logger: The configured application logger.
    
    Example:
        from bot.logging_config import get_logger
        
        logger = get_logger()
        logger.info("Order placed successfully")
        logger.warning("Validation failed")
        logger.error("API connection error")
    """
    global _logger
    
    if _logger is None:
        _logger = _configure_logger()
    
    return _logger
