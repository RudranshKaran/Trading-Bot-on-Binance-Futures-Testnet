# Architecture Overview

## 1. Purpose of This Document

This document describes the architecture of the **Binance Futures Testnet Trading Bot**, a Python-based application that supports both **CLI-driven** and **Streamlit-based UI** interactions for placing orders on Binance Futures Testnet.

The architecture is designed to demonstrate:
- Clean separation of concerns
- Reusable backend logic
- Multiple interface layers (CLI + UI) over a shared core
- Production-style logging and error handling

---

## 2. Architectural Design Goals

The system is built around the following principles:

- **Interface Independence**  
  Business logic is completely decoupled from user interfaces (CLI or Streamlit).

- **Single Source of Truth**  
  Order execution, validation, and API interaction live in one shared backend.

- **Extensibility**  
  New interfaces, order types, or exchanges can be added without refactoring core logic.

- **Observability & Reliability**  
  All critical actions, API calls, and failures are logged consistently.

---

## 3. High-Level System Flow

The application supports **two entry points**: CLI and Streamlit UI.


```
      ┌──────────────┐
      │     CLI      │
      └──────┬───────┘
             │
      ┌──────▼───────┐
      │  Validation  │
      └──────┬───────┘
             │
      ┌──────▼───────┐
      │ Order Logic  │
      └──────┬───────┘
             │
      ┌──────▼───────┐
      │ Binance API  │
      └──────┬───────┘
             │
    Console Output + Logs
```
```
      ┌──────────────┐
      │  Streamlit   │
      └──────┬───────┘
             │
      ┌──────▼───────┐
      │  Validation  │
      └──────┬───────┘
             │
      ┌──────▼───────┐
      │ Order Logic  │
      └──────┬───────┘
             │
      ┌──────▼───────┐
      │ Binance API  │
      └──────┬───────┘
             │
     UI Feedback + Logs
```

Both interfaces rely on the **same backend modules**, ensuring consistency and reliability.

---

## 4. Project Structure Overview

```

trading_bot/
│
├── bot/                          # Core backend logic (interface-agnostic)
│   ├── client.py                 # Binance Futures API client wrapper
│   ├── orders.py                 # Order execution logic
│   ├── validators.py             # Input validation logic
│   ├── logging_config.py         # Centralized logging configuration
│   └── **init**.py
│
├── interfaces/
│   ├── cli.py                    # CLI entry point
│   └── streamlit_app.py          # Streamlit UI interface
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CLI_USAGE.md
│   ├── LOGGING.md
│   └── ASSUMPTIONS.md
│
├── logs/
│   └── trading_bot.log
│
├── README.md
├── requirements.txt

```

---

## 5. Backend Core Modules (`bot/`)

### 5.1 `client.py` — Binance API Client Layer

**Responsibility:**
- Manages all communication with Binance Futures Testnet
- Encapsulates API-specific details

**Key Responsibilities:**
- Client initialization using API credentials
- Sending market and limit order requests
- Handling API-level exceptions
- Returning structured responses to calling layers

This module ensures that external dependencies remain isolated.

---

### 5.2 `orders.py` — Order Execution Logic

**Responsibility:**
- Contains core business logic for order placement
- Acts as the orchestration layer between validation and API calls

**Responsibilities Include:**
- Determining order type (MARKET / LIMIT)
- Preparing request payloads
- Executing orders via the client layer
- Normalizing responses for both CLI and UI consumption

This module is intentionally interface-agnostic.

---

### 5.3 `validators.py` — Input Validation Layer

**Responsibility:**
- Validates all inputs before any order execution

**Validation Rules Include:**
- Valid trading symbol format
- Side must be `BUY` or `SELL`
- Order type must be `MARKET` or `LIMIT`
- Price is mandatory for LIMIT orders
- Quantity and price must be positive values

Fail-fast validation prevents invalid API calls and improves user feedback.

---

### 5.4 `logging_config.py` — Centralized Logging

**Responsibility:**
- Provides a unified logging configuration across the application

**Logging Characteristics:**
- File-based logging
- Structured, timestamped entries
- Standard log levels (`INFO`, `WARNING`, `ERROR`)

All modules import this configuration to ensure consistent logging behavior.

---

## 6. Interface Layers (`interfaces/`)

### 6.1 `cli.py` — Command-Line Interface

**Responsibility:**
- Parses command-line arguments
- Displays formatted console output
- Delegates all processing to backend modules

**Key Characteristics:**
- Contains no business logic
- Focuses only on user interaction and presentation
- Ideal for automation, scripting, and testing

---

### 6.2 `streamlit_app.py` — Streamlit User Interface

**Responsibility:**
- Provides a lightweight graphical interface for order placement
- Improves accessibility and usability for non-CLI users

**Key Characteristics:**
- Uses form-based inputs for order parameters
- Displays order results and error messages in real time
- Calls the same backend functions used by the CLI

The Streamlit layer acts strictly as a **presentation layer**, not a logic layer.

---

## 7. Error Handling Strategy

The application follows a layered error-handling approach:

### 7.1 Validation Errors
- Detected in the validation layer
- Reported immediately to CLI or UI
- Logged as warnings

### 7.2 API Errors
- Handled in the client layer
- Includes rejected orders, authentication failures, or insufficient balance
- Logged with detailed API responses

### 7.3 Runtime & Network Errors
- Includes timeouts or connectivity issues
- Logged with stack traces
- User-facing messages remain clean and readable

---

## 8. Logging Strategy Overview

The logging system captures:
- User order requests
- API payloads and responses
- Validation failures
- Execution errors

This ensures:
- Traceability of actions
- Easier debugging
- Compliance with assignment requirements

Detailed logging behavior is described in `LOGGING.md`.

---

## 9. Extensibility Considerations

This architecture allows for:
- Adding new order types with minimal changes
- Introducing additional interfaces (e.g., REST API)
- Supporting new exchanges via additional client modules
- Running the same backend logic across multiple entry points

---

## 10. Summary

The system architecture cleanly separates **core trading logic** from **user interfaces**, enabling both CLI-based automation and Streamlit-based interactivity.  
This design balances simplicity with production-oriented practices, making it well-suited for demonstrating backend engineering skills in a real-world API integration scenario.