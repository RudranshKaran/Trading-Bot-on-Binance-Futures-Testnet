"""
Binance Futures Testnet Client Wrapper

This module provides a thin wrapper around the Binance Futures Testnet API.
It encapsulates all API interactions and handles credential management,
connectivity testing, and error handling.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.logging_config import get_logger


# Binance Futures Testnet configuration
TESTNET_BASE_URL = "https://testnet.binancefuture.com"

# Environment variable names
ENV_API_KEY = "BINANCE_API_KEY"
ENV_API_SECRET = "BINANCE_API_SECRET"


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""
    pass


class BinanceTestnetClient:
    """
    Binance Futures Testnet API client wrapper.
    
    This class encapsulates all interactions with the Binance Futures Testnet,
    providing a clean interface for the rest of the application.
    
    Attributes:
        client: The underlying python-binance Client instance.
        logger: The centralized application logger.
    
    Example:
        client = BinanceTestnetClient()
        if client.test_connection():
            print("Connected to Binance Futures Testnet")
    """
    
    def __init__(self) -> None:
        """
        Initialize the Binance Futures Testnet client.
        
        Loads API credentials from environment variables and initializes
        the client connection to the testnet.
        
        Raises:
            ConfigurationError: If required environment variables are missing.
        """
        self.logger = get_logger()
        self._client: Client  # Initialized in _initialize_client()
        
        # Load environment variables from .env file if present
        load_dotenv()
        
        # Load and validate credentials
        self._api_key = self._get_required_env(ENV_API_KEY)
        self._api_secret = self._get_required_env(ENV_API_SECRET)
        
        # Initialize the client
        self._initialize_client()
    
    def _get_required_env(self, var_name: str) -> str:
        """
        Get a required environment variable.
        
        Args:
            var_name: Name of the environment variable.
            
        Returns:
            The value of the environment variable.
            
        Raises:
            ConfigurationError: If the environment variable is not set or empty.
        """
        value = os.getenv(var_name)
        
        if not value:
            error_msg = (
                f"Missing required environment variable: {var_name}. "
                f"Please set {var_name} in your environment or .env file."
            )
            self.logger.error(f"Configuration error: {error_msg}")
            raise ConfigurationError(error_msg)
        
        return value
    
    def _initialize_client(self) -> None:
        """
        Initialize the Binance client with testnet configuration.
        
        Configures the client to use the Futures Testnet endpoints.
        """
        try:
            self._client = Client(
                api_key=self._api_key,
                api_secret=self._api_secret,
                testnet=True
            )
            
            # Configure for Futures Testnet
            self._client.FUTURES_URL = TESTNET_BASE_URL
            
            self.logger.info("Binance Futures Testnet client initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Binance client: {e}")
            raise
    
    @property
    def client(self) -> Client:
        """
        Get the underlying Binance client instance.
        
        Returns:
            The python-binance Client instance.
        """
        return self._client
    
    def test_connection(self) -> bool:
        """
        Test connectivity to Binance Futures Testnet.
        
        Sends a ping request to verify that the API is reachable
        and the client is properly configured.
        
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            # Use futures ping endpoint to test connectivity
            self._client.futures_ping()
            self.logger.info(
                "Connection test successful: Binance Futures Testnet is reachable"
            )
            return True
            
        except BinanceAPIException as e:
            self.logger.error(
                f"API error during connection test: "
                f"Code={e.code} Message={e.message}"
            )
            return False
            
        except BinanceRequestException as e:
            self.logger.error(f"Request error during connection test: {e}")
            return False
            
        except Exception as e:
            self.logger.error(f"Unexpected error during connection test: {e}")
            return False
    
    def get_server_time(self) -> Optional[dict]:
        """
        Get the current server time from Binance Futures Testnet.
        
        This can be used to verify connectivity and check for
        time synchronization issues.
        
        Returns:
            dict: Server time response, or None if the request fails.
        """
        try:
            server_time = self._client.futures_time()
            self.logger.info(f"Server time retrieved: {server_time}")
            return server_time
            
        except BinanceAPIException as e:
            self.logger.error(
                f"API error getting server time: Code={e.code} Message={e.message}"
            )
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting server time: {e}")
            return None
    
    def place_order(self, **kwargs) -> dict:
        """
        Place an order on Binance Futures Testnet.
        
        This is a placeholder method for Phase 3 implementation.
        Full order execution logic will be added in the orders.py module.
        
        Args:
            **kwargs: Order parameters (symbol, side, type, quantity, etc.)
            
        Returns:
            dict: Order response from the API.
            
        Raises:
            NotImplementedError: This method is a placeholder for Phase 3.
        """
        raise NotImplementedError(
            "Order placement will be implemented in Phase 3. "
            "See bot/orders.py for the complete implementation."
        )
