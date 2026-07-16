# Ledger CLI

Ledger CLI is a command-line double-entry accounting application built with Python. It allows users to record journal entries, generate a trial balance, view the general ledger, and check account balances.

## Features

- Record balanced journal entries
- Generate a Trial Balance
- View the General Ledger
- Check account balances
- Store transactions in JSON format

## Installation

```bash
git clone https://github.com/samarjs/ledger-cli.git
cd ledger-cli
python main.py
```

## Commands

| Command | Description |
|---------|-------------|
| `add "Description" DD/MM/YYYY Account Amount Dr Account Amount Cr` | Record a transaction |
| `list` | View all transactions |
| `trial` | Display the Trial Balance |
| `ledger` | Display the General Ledger |
| `balance <account>` | Show an account balance |
| `help` | Display available commands |
| `exit` | Close the application |

## Example

```text
ledger> add "Office Rent" 16/07/2026 Rent 500 Dr Cash 500 Cr

✓ Transaction added successfully!

ledger> trial

Cash      500.00 Cr
Rent      500.00 Dr

Total Debits   500.00
Total Credits  500.00
```

## Project Structure

```
ledger-cli/
├── data/
├── ledger/
├── main.py
└── README.md
```

## Author

**Samar**

GitHub: https://github.com/samarjs