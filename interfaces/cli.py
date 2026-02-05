#!/usr/bin/env python3
"""
CLI Entry Point for Binance Futures Testnet Trading Bot.

This module provides a command-line interface for placing MARKET and LIMIT
orders on Binance Futures Testnet. All business logic is delegated to the
backend modules in the `bot` package.

Usage:
    python interfaces/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
    python interfaces/cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 45000
"""

import argparse
import sys
from pathlib import Path

# Add project root to Python path for module resolution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from bot import (
    get_logger,
    place_market_order,
    place_limit_order,
    ValidationError,
    OrderExecutionError,
    ConfigurationError,
)


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="trading-bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        epilog="Example: python interfaces/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--symbol",
        required=True,
        type=str,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)",
    )

    parser.add_argument(
        "--side",
        required=True,
        type=str,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL",
    )

    parser.add_argument(
        "--type",
        required=True,
        type=str,
        dest="order_type",
        choices=["MARKET", "LIMIT", "market", "limit"],
        help="Order type: MARKET or LIMIT",
    )

    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity (positive number)",
    )

    parser.add_argument(
        "--price",
        required=False,
        type=float,
        default=None,
        help="Limit price (required for LIMIT orders)",
    )

    return parser


def print_order_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
) -> None:
    """
    Print a formatted order request summary to the terminal.

    Args:
        symbol: Trading pair symbol.
        side: Order side (BUY/SELL).
        order_type: Order type (MARKET/LIMIT).
        quantity: Order quantity.
        price: Limit price (optional).
    """
    print("\nOrder Request Summary")
    print("-" * 21)
    print(f"Symbol      : {symbol}")
    print(f"Side        : {side}")
    print(f"Order Type  : {order_type}")
    print(f"Quantity    : {quantity}")
    if order_type.upper() == "LIMIT" and price is not None:
        print(f"Limit Price : {price}")
    print()


def print_order_response(response: dict) -> None:
    """
    Print a formatted order response to the terminal.

    Args:
        response: Normalized order response dictionary.
    """
    print("Order placed successfully!")
    print(f"Order ID          : {response.get('order_id', 'N/A')}")
    print(f"Order Status      : {response.get('status', 'N/A')}")
    print(f"Executed Quantity : {response.get('executed_qty', 'N/A')}")

    avg_price = response.get("avg_price")
    if avg_price is not None and float(avg_price) > 0:
        print(f"Average Price     : {avg_price}")

    print()


def print_error(message: str) -> None:
    """
    Print a formatted error message to the terminal.

    Args:
        message: Error message to display.
    """
    print(f"\nError: {message}\n", file=sys.stderr)


def main() -> int:
    """
    Main entry point for the CLI application.

    Returns:
        int: Exit code (0 for success, non-zero for failure).
    """
    logger = get_logger()

    # Parse command-line arguments
    parser = create_parser()
    args = parser.parse_args()

    # Normalize inputs to uppercase
    symbol = args.symbol.upper()
    side = args.side.upper()
    order_type = args.order_type.upper()
    quantity = args.quantity
    price = args.price

    # Log the incoming request
    logger.info(
        f"CLI order request received | "
        f"Symbol={symbol} Side={side} Type={order_type} "
        f"Quantity={quantity} Price={price} Source=CLI"
    )

    # Print order summary
    print_order_summary(symbol, side, order_type, quantity, price)

    try:
        # Execute the order based on type
        if order_type == "MARKET":
            response = place_market_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
            )
        else:  # LIMIT
            response = place_limit_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price,
            )

        # Log and print success
        logger.info(
            f"Order placed successfully | "
            f"OrderID={response.get('order_id')} "
            f"Status={response.get('status')} "
            f"ExecutedQty={response.get('executed_qty')} "
            f"AvgPrice={response.get('avg_price')}"
        )
        print_order_response(response)
        return 0

    except ValidationError as e:
        error_msg = e.message if hasattr(e, "message") else str(e)
        field_info = f" (field: {e.field})" if hasattr(e, "field") and e.field else ""
        logger.warning(f"Validation failed | Reason={error_msg}{field_info} Source=CLI")
        print_error(error_msg)
        return 1

    except ConfigurationError as e:
        error_msg = str(e)
        logger.error(f"Configuration error | Reason={error_msg}")
        print_error(f"Configuration error: {error_msg}")
        print("Please ensure BINANCE_API_KEY and BINANCE_API_SECRET environment variables are set.")
        return 1

    except OrderExecutionError as e:
        error_msg = e.message if hasattr(e, "message") else str(e)
        error_code = f" (code: {e.error_code})" if hasattr(e, "error_code") and e.error_code else ""
        logger.error(f"Order execution failed | Reason={error_msg}{error_code}")
        print_error(f"Order execution failed: {error_msg}")
        return 1

    except KeyboardInterrupt:
        logger.info("CLI execution interrupted by user")
        print("\nOperation cancelled by user.")
        return 130

    except Exception as e:
        logger.exception(f"Unexpected error during CLI execution | Error={e}")
        print_error(f"An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
