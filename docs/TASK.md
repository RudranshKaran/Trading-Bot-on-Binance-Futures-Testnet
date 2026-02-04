# Task Description — Python Developer Internship Assignment

## Application Task  
**Role:** Python Developer Intern  
**Estimated Time:** Less than 60 minutes  

This document contains the original task description provided as part of the internship application process.  
It is included in this repository for clarity, traceability, and reference.

---

## Objective

Build a **simplified trading bot** using Python that can place orders on **Binance Futures Testnet (USDT-M)**.

The application should demonstrate:
- Clean and reusable code structure
- Proper logging
- Robust error handling
- Ability to interact with a real external API (testnet environment)

---

## Setup Requirements

1. Register and activate a **Binance Futures Testnet** account.
2. Generate API credentials (API Key and Secret).
3. Use the following base URL for all API interactions:

```

[https://testnet.binancefuture.com](https://testnet.binancefuture.com)

```

4. You may use **either** of the following approaches:
   - `python-binance` library  
   - Direct REST API calls using `requests` or `httpx`

---

## Core Requirements (Must-Have)

### Language
- Python 3.x

---

### Functional Requirements

The application must:

1. Place **Market** and **Limit** orders on Binance Futures Testnet (USDT-M).
2. Support both order sides:
   - `BUY`
   - `SELL`
3. Accept and validate user input via a **Command-Line Interface (CLI)** using tools such as:
   - `argparse`
   - `Typer`
   - `Click`

---

### Required CLI Inputs

| Input | Description | Example |
|-----|------------|---------|
| `symbol` | Trading pair | `BTCUSDT` |
| `side` | Order side | `BUY` / `SELL` |
| `order type` | Type of order | `MARKET` / `LIMIT` |
| `quantity` | Order quantity | `0.01` |
| `price` | Required only for LIMIT orders | `45000` |

---

### Output Requirements

The application must print **clear and readable output**, including:

- Order request summary
- Order response details:
  - `orderId`
  - `status`
  - `executedQty`
  - `avgPrice` (if available)
- Explicit success or failure message

---

### Code Quality Requirements

The application must implement:

- Structured code with clear separation of concerns:
  - Client / API layer
  - Command / CLI layer
- Logging of:
  - API requests
  - API responses
  - Errors
- Exception handling for:
  - Invalid user input
  - API errors
  - Network failures

---

## Deliverables

Submit **either**:

### Option 1
- A **public GitHub repository** (preferred)

### Option 2
- A zip archive containing:
  - Source code
  - Documentation
  - Log files

---

### Required Files

Your submission must include:

1. Source code
2. `README.md` containing:
   - Setup steps
   - Usage examples
   - Assumptions
3. `requirements.txt` (or `pyproject.toml`)
4. Log files from:
   - At least one **MARKET** order
   - At least one **LIMIT** order

---

## Bonus (Optional — Choose Any One)

You may optionally implement **one** of the following:

- Add a third order type:
  - Stop-Limit
  - OCO
  - TWAP
  - Grid
- Enhance CLI UX:
  - Menus
  - Prompts
  - Better validation messages
- Add a lightweight UI

---

## Suggested Project Structure (Optional)

```

trading_bot/
├── bot/
│   ├── **init**.py
│   ├── client.py        # Binance client wrapper
│   ├── orders.py        # Order placement logic
│   ├── validators.py   # Input validation
│   ├── logging_config.py
│   └── cli.py           # CLI entry point
├── README.md
├── requirements.txt

```

---

## Evaluation Criteria

Submissions are evaluated based on:

- **Correctness**  
  Successful order placement on testnet

- **Code Quality**  
  Readability, structure, and reusability

- **Validation & Error Handling**

- **Logging Quality**  
  Useful, structured, and non-noisy logs

- **Documentation Quality**  
  Clear README and runnable instructions

---

## Submission Instructions

Email the following:
- Resume
- Submission link (GitHub repository or zip)
- Log files

To:
- joydip@anything.ai  
- chetan@anything.ai  
- hello@anything.ai  

**CC:** sonika@anything.ai

---

## Notes

- This project is intended strictly for evaluation purposes.
- All trading must be performed on **Binance Futures Testnet** only.
- No real funds should be used.