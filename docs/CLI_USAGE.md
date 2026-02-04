# CLI Usage Guide

## 1. Overview

This document describes how to use the **Command-Line Interface (CLI)** for the Binance Futures Testnet Trading Bot.

The CLI provides a lightweight, scriptable way to place **Market** and **Limit** orders on Binance Futures Testnet using validated user inputs and consistent backend logic.

---

## 2. CLI Entry Point

The CLI is implemented in:

```
interfaces/cli.py
````

All CLI commands invoke shared backend logic located in the `bot/` module.

---

## 3. Prerequisites

Before using the CLI, ensure the following:

- Python 3.9 or higher is installed
- Dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

* Binance Futures Testnet API credentials are available as environment variables:

  ```bash
  export BINANCE_API_KEY="your_testnet_api_key"
  export BINANCE_API_SECRET="your_testnet_api_secret"
  ```

---

## 4. General Command Format

The CLI accepts inputs via command-line flags.

```
python interfaces/cli.py \
  --symbol <SYMBOL> \
  --side <BUY|SELL> \
  --type <MARKET|LIMIT> \
  --quantity <QUANTITY> \
  [--price <PRICE>]
```

---

## 5. Supported Parameters

| Parameter    | Required    | Description                      |
| ------------ | ----------- | -------------------------------- |
| `--symbol`   | Yes         | Trading pair (e.g., `BTCUSDT`)   |
| `--side`     | Yes         | Order side: `BUY` or `SELL`      |
| `--type`     | Yes         | Order type: `MARKET` or `LIMIT`  |
| `--quantity` | Yes         | Order quantity (positive number) |
| `--price`    | Conditional | Required only for LIMIT orders   |

---

## 6. Order Types

### 6.1 Market Order

A **Market order** executes immediately at the best available market price.

#### Example

```bash
python interfaces/cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.01
```

#### Expected Output

```
Order Request Summary
---------------------
Symbol      : BTCUSDT
Side        : BUY
Order Type  : MARKET
Quantity    : 0.01

Order placed successfully!
Order ID          : 123456789
Order Status      : FILLED
Executed Quantity : 0.01
Average Price     : 43215.75
```

---

### 6.2 Limit Order

A **Limit order** is placed at a specific price and executes only when the market reaches that price.

#### Example

```bash
python interfaces/cli.py \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.01 \
  --price 45000
```

#### Expected Output

```
Order Request Summary
---------------------
Symbol      : BTCUSDT
Side        : SELL
Order Type  : LIMIT
Quantity    : 0.01
Limit Price : 45000

Order placed successfully!
Order ID     : 987654321
Order Status : NEW
```

---

## 7. Input Validation Rules

All inputs are validated before any API call is made.

### Validation Constraints

* `symbol` must be a non-empty string (e.g., `BTCUSDT`)
* `side` must be either `BUY` or `SELL`
* `type` must be either `MARKET` or `LIMIT`
* `quantity` must be a positive number
* `price` must be:

  * provided for LIMIT orders
  * a positive number

---

## 8. Validation Error Examples

### Missing Price for LIMIT Order

```bash
python interfaces/cli.py \
  --symbol BTCUSDT \
  --side BUY \
  --type LIMIT \
  --quantity 0.01
```

**Output:**

```
Error: Price is required for LIMIT orders.
```

---

### Invalid Order Side

```bash
python interfaces/cli.py \
  --symbol BTCUSDT \
  --side HOLD \
  --type MARKET \
  --quantity 0.01
```

**Output:**

```
Error: Invalid order side. Allowed values are BUY or SELL.
```

---

## 9. Error Handling Behavior

* Validation errors are caught before API calls
* API errors are displayed with a user-friendly message
* Detailed error information is written to the log file
* The CLI exits gracefully without uncaught exceptions

---

## 10. Logging Behavior

Every CLI execution logs:

* Order request details
* API responses
* Validation failures
* Execution errors

Logs are written to:

```
logs/trading_bot.log
```

For detailed logging behavior, refer to `LOGGING.md`.

---

## 11. Best Practices

* Always verify inputs before executing an order
* Use Market orders for quick testing
* Check logs when troubleshooting unexpected behavior
* Avoid committing API keys to source control

---

## 12. Summary

The CLI provides a robust, scriptable interface for interacting with Binance Futures Testnet.
It is designed to be simple for manual use, reliable for automation, and consistent with backend business logic shared across all interfaces.