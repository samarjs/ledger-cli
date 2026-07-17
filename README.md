# Ledger CLI

A Python double-entry accounting application with both **command-line** and **web** interfaces. Record journal entries, maintain ledgers, generate trial balances, and view reports — all from your terminal or browser.

---

## Live Demo

**Web App:** https://ledger-cli.onrender.com

The web app is deployed on Render's free tier. Note: Free instances spin down after inactivity, so the first load may take ~50 seconds.

---

## Features

### Version 1.0 ✅
- Record balanced journal entries (Debits must equal Credits)
- Support for account names with spaces (use quotes like `"Rent Expense"`)
- Generate a Trial Balance
- View the General Ledger
- Check individual account balances
- Delete transactions by ID
- Colorized terminal output
- Sequential transaction IDs (TXN-00001, TXN-00002, etc.)
- Decimal precision for money (no floating-point rounding errors)
- Persistent JSON storage
- Input validation (rejects negative amounts, zero amounts, unbalanced entries)
- Graceful handling of corrupted JSON files
- Unit tests included

### Version 1.1 ✅ (Current)
- Web interface (Flask) deployed to Render
- Add transactions via browser
- View Trial Balance and General Ledger online

### Version 1.2 (Planned)
- Edit existing transactions
- Search/filter transactions by keyword or date
- Export reports to CSV
- Undo last transaction

### Future Releases
- Multiple currency support
- Budget tracking
- Data import from Excel/CSV
- GitHub Actions CI/CD

---

## CLI Usage

### Installation
```bash
git clone https://github.com/samarjs/ledger-cli.git
cd ledger-cli
pip install -r requirements.txt
python main.py
