# Assumptions & Design Decisions

## 1. Purpose of This Document

This document outlines the assumptions and deliberate design decisions made while building the **Binance Futures Testnet Trading Bot**.

These assumptions help:
- Clarify the intended scope of the application
- Explain trade-offs made during implementation
- Avoid ambiguity during evaluation or interviews

---

## 2. Environment Assumptions

- The application is intended to run **only on Binance Futures Testnet**.
- All trades are executed using **testnet funds**.
- No real-money trading is supported or intended.
- The Binance Futures Testnet base URL is fixed and not configurable at runtime.

---

## 3. Market & Instrument Assumptions

- Only **USDT-M Futures contracts** are supported.
- Trading symbols are assumed to be valid Binance Futures symbols (e.g., `BTCUSDT`).
- Symbol discovery and validation via exchange metadata is not implemented to keep the scope focused.

---

## 4. Order Execution Assumptions

- Supported order types are limited to:
  - `MARKET`
  - `LIMIT`
- Only one order is placed per execution.
- Advanced order types (e.g., Stop-Limit, OCO, Grid) are intentionally excluded unless added as a bonus feature.
- Partial fills are handled as returned by the Binance API without additional logic.

---

## 5. Position & Risk Management Assumptions

- Leverage configuration is not managed by the application.
- Margin type (isolated / cross) is not configured or modified.
- Position sizing logic is not implemented.
- The application does not calculate profit, loss, or exposure.

These aspects are outside the scope of the assignment and trading strategy concerns.

---

## 6. Input Assumptions

- Users provide syntactically correct inputs via CLI or Streamlit UI.
- Inputs are validated for correctness but not normalized beyond basic checks.
- Quantity and price values are assumed to comply with Binance precision rules.

---

## 7. Authentication & Configuration Assumptions

- API credentials are provided via environment variables:
  - `BINANCE_API_KEY`
  - `BINANCE_API_SECRET`
- API keys are assumed to have sufficient permissions for trading on the testnet.
- Credential rotation and multi-account support are not implemented.

---

## 8. Error Handling Assumptions

- Validation errors are treated as user errors and fail fast.
- API and network errors are surfaced cleanly to the user and logged.
- Retry logic for failed API calls is not implemented to keep behavior predictable.

---

## 9. Logging Assumptions

- Logging is primarily intended for development and debugging.
- Log files may grow over time; log rotation is not implemented.
- Logs are stored locally and not shipped to external monitoring systems.

---

## 10. Interface Assumptions

- Both CLI and Streamlit interfaces are considered **thin presentation layers**.
- All business logic is centralized in the backend core.
- Interfaces do not maintain state across executions or sessions.

---

## 11. Security Assumptions

- API keys and secrets are never logged or exposed in outputs.
- The project is not hardened for production deployment.
- No authentication or access control is implemented at the interface level.

---

## 12. Scalability Assumptions

- The application is designed for single-user, single-process execution.
- Concurrent order placement is not supported.
- Performance optimization is not a primary concern due to limited scope.

---

## 13. Future Enhancements (Out of Scope)

The following improvements are intentionally left out but are compatible with the current architecture:

- Support for additional order types
- Exchange metadata validation
- Leverage and margin configuration
- Trade history tracking
- Production-grade monitoring and alerting

---

## 14. Summary

These assumptions reflect a conscious effort to balance **clarity, correctness, and scope control**.  
The project focuses on demonstrating clean architecture, API integration, validation, and logging rather than implementing full-scale trading functionality.
