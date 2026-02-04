# Logging Guide

## 1. Overview

This document describes the logging strategy used in the **Binance Futures Testnet Trading Bot**.

Logging is treated as a first-class concern in this project to ensure:
- Observability of system behavior
- Traceability of order execution
- Easier debugging of failures
- Compliance with the assignment’s logging requirements

All application logs are centralized and written to a dedicated log file.

---

## 2. Logging Objectives

The logging system is designed to:

- Record all order requests and responses
- Capture validation and runtime errors
- Provide meaningful diagnostic information without being noisy
- Remain consistent across multiple interfaces (CLI and Streamlit)

---

## 3. Log File Location

All logs are written to the following location:

```

logs/trading_bot.log

```

The log directory is created automatically if it does not exist.

---

## 4. Logging Configuration

Logging is configured centrally in:

```

bot/logging_config.py

```

### Configuration Characteristics

- Single global logger shared across all modules
- File-based logging
- Timestamped log entries
- Consistent formatting across the application

All modules import and use this configuration to avoid duplication.

---

## 5. Log Levels Used

The application uses the following standard log levels:

| Level | Usage |
|------|------|
| INFO | Successful operations and normal execution flow |
| WARNING | Recoverable issues and validation failures |
| ERROR | API failures, runtime errors, and unexpected exceptions |

This level separation ensures clarity while debugging and reviewing logs.

---

## 6. What Gets Logged

### 6.1 Order Requests

Before sending any request to Binance, the following details are logged:

- Trading symbol
- Order side (BUY / SELL)
- Order type (MARKET / LIMIT)
- Quantity
- Price (if applicable)
- Interface source (CLI or Streamlit)

**Purpose:**  
To provide traceability for every attempted order.

---

### 6.2 API Requests & Responses

The following are logged:

- API endpoint invoked
- Request payload (sanitized)
- Response status
- Response payload (order ID, status, execution details)

**Purpose:**  
To diagnose API-related issues and verify successful interactions.

---

### 6.3 Validation Errors

When user input fails validation, logs include:

- Invalid field name
- Reason for validation failure
- Interface source

**Log Level:** `WARNING`

**Purpose:**  
To detect incorrect usage patterns and prevent unnecessary API calls.

---

### 6.4 API Errors

Examples include:

- Invalid API credentials
- Insufficient balance
- Order rejection by exchange

**Log Level:** `ERROR`

**Purpose:**  
To capture actionable failure details returned by the exchange.

---

### 6.5 Runtime & Network Errors

Examples include:

- Network timeouts
- Connection failures
- Unexpected exceptions

**Log Level:** `ERROR`

Stack traces are logged to assist with root-cause analysis.

---

## 7. Sample Log Entries

### 7.1 Successful Market Order

```

2025-02-06 10:14:22 | INFO | Order request received
Symbol=BTCUSDT Side=BUY Type=MARKET Quantity=0.01 Source=CLI

2025-02-06 10:14:23 | INFO | Order placed successfully
OrderID=123456789 Status=FILLED ExecutedQty=0.01 AvgPrice=43215.75

```

---

### 7.2 Successful Limit Order

```

2025-02-06 10:17:48 | INFO | Order request received
Symbol=BTCUSDT Side=SELL Type=LIMIT Quantity=0.01 Price=45000 Source=Streamlit

2025-02-06 10:17:48 | INFO | Limit order placed
OrderID=987654321 Status=NEW

```

---

### 7.3 Validation Failure

```

2025-02-06 10:20:11 | WARNING | Validation failed
Reason=Price is required for LIMIT orders Source=CLI

```

---

### 7.4 API Error

```

2025-02-06 10:22:05 | ERROR | API error during order placement
ErrorCode=-2015 Message=Invalid API-key, IP, or permissions

```

---

### 7.5 Network Error

```

2025-02-06 10:25:37 | ERROR | Network failure
Exception=ConnectionTimeout StackTrace=...

```

---

## 8. Logging Across Interfaces

Both CLI and Streamlit interfaces use the same logging system.

This ensures:
- Unified log format
- Single source of truth
- Easier correlation between UI actions and backend behavior

The interface source is included in log entries when applicable.

---

## 9. Security Considerations

- API keys and secrets are never logged
- Sensitive data is excluded or sanitized before logging
- Logs are intended for development and debugging in a testnet environment only

---

## 10. Log Retention & Management

- Logs are appended to a single file per execution environment
- Log rotation is not implemented due to the limited scope of the assignment
- Rotation can be added easily if extended to production use

---

## 11. Assignment Compliance

This logging implementation satisfies the assignment requirement to submit:

- Log output from at least one MARKET order
- Log output from at least one LIMIT order

These logs demonstrate successful API interaction and proper observability.

---

## 12. Summary

The logging system provides clear visibility into application behavior, captures critical execution details, and supports both CLI and UI interfaces uniformly.  
It is intentionally lightweight yet structured, reflecting production-aware backend development practices.
