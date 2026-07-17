# Ledger CLI

Ledger CLI is a command-line double-entry accounting application built with Python. It allows users to record journal entries, generate a trial balance, view the general ledger, and check account balances.

## Features

- Record balanced journal entries (Debits must equal Credits)
- Support for account names with spaces (use quotes like "Rent Expense")
- Generate a Trial Balance
- View the General Ledger
- Check individual account balances
- Delete transactions by ID
- Colorized terminal output (green for success, red for errors, blue headers)
- Sequential transaction IDs (TXN-00001, TXN-00002, etc.)
- Decimal precision for money (no floating-point rounding errors)
- Persistent JSON storage
- Input validation (rejects negative amounts, zero amounts, unbalanced entries)
- Graceful handling of corrupted JSON files
- Unit tests included

## Installation

```bash
git clone https://github.com/samarjs/ledger-cli.git
cd ledger-cli
python main.py
```

## Commands

| Command                                                                   | Description                      |
| ------------------------------------------------------------------------- | -------------------------------- |
| `add "Description" DD/MM/YYYY Account Amount Dr Account Amount Cr`        | Record a transaction             |
| `list`                                                                    | View all transactions            |
| `trial`                                                                   | Display the Trial Balance        |
| `ledger`                                                                  | Display the General Ledger       |
| `balance <account>`                                                       | Show an account balance          |
| `delete <id>`                                                             | Delete a transaction by ID       |
| `help`                                                                    | Display available commands       |
| `exit`                                                                    | Close the application            |


## Example

```text
ledger> add "Office Rent" 16/07/2026 "Rent Expense" 500 Dr Cash 500 Cr

✓ Transaction added successfully!
   ID: TXN-00001
   Date: 2026-07-16
   Description: Office Rent
   Rent Expense: 500.00 debit
   Cash: 500.00 credit
```

## Project Structure

```
ledger-cli/
├── data/                      # Transaction storage (gitignored)
│   └── ledger.json
├── ledger/                    # Core package
│   ├── __init__.py
│   ├── colors.py              # Terminal color utilities
│   ├── models.py              # Entry and Transaction dataclasses
│   ├── engine.py              # Core ledger logic
│   ├── storage.py             # JSON persistence
│   └── reports.py             # Report generation
├── tests/                     # Unit tests
│   └── test_ledger.py
├── main.py                    # CLI entry point
├── pyproject.toml             # Package configuration
├── .gitignore
└── README.md
```

## Running Tests
```
python -m unittest tests.test_ledger -v
```
## Author

**Samar**

GitHub: https://github.com/samarjs
