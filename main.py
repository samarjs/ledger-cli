#!/usr/bin/env python3
import sys
import os
import shlex
from datetime import datetime
from decimal import Decimal
from ledger.models import Entry
from ledger.engine import LedgerEngine
from ledger.storage import Storage
from ledger.reports import ReportGenerator

def print_help():
    print("""
+------------------------------------------------------------------------------+
|               LEDGER CLI - Double-Entry Accounting System                    |
+------------------------------------------------------------------------------+
|                                                                              |
|  Commands                                                                    |
+------------------------------------------------------------------------------+
| add "Description" DD/MM/YYYY Account1 Amount1 Dr Account2 Amount2 Cr         |
|                                                                              |
|  Account names with spaces must be in quotes:                                |
|  add "Office Rent" 16/07/2026 "Rent Expense" 500 Dr Cash 500 Cr              |
|                                                                              |
| Example:                                                                     |
| ledger> add "Office Rent" 16/07/2026 Rent 500 Dr Cash 500 Cr                 |
|                                                                              |
| This records:                                                                |
|   Rent  500.00 Dr                                                            |
|   Cash  500.00 Cr                                                            |
|                                                                              |
| Transactions are automatically saved in:                                     |
|   data/ledger.json                                                           |
+------------------------------------------------------------------------------+
| trial                  Show the Trial Balance                                |
| ledger                 Show the General Ledger                               |
| balance <account>      Show the balance of an account                        |
| list                   View all recorded transactions                        |
| delete <id>            Delete a transaction by ID                            |
| help                   Display this help menu                                |
| exit                   Exit the application                                  |
+------------------------------------------------------------------------------+
""")

def parse_date(date_str):
    try:
        day, month, year = date_str.split("/")
        datetime(int(year), int(month), int(day))
        return f"{year}-{month}-{day}"
    except ValueError:
        raise ValueError(f"Invalid date '{date_str}'. Use DD/MM/YYYY format.")
    except Exception:
        return date_str

def parse_add_command(rest):
    if '"' not in rest:
        raise ValueError("Description must be in quotes")
    start_quote = rest.find('"')
    end_quote = rest.find('"', start_quote + 1)
    if end_quote == -1:
        raise ValueError("Closing quote not found for description")
    description = rest[start_quote + 1:end_quote]
    after_desc = rest[end_quote + 1:].strip()
    try:
        tokens = shlex.split(after_desc)
    except ValueError as e:
        raise ValueError(f"Error parsing command: {e}")
    if len(tokens) < 5:
        raise ValueError("Not enough arguments. Need: DD/MM/YYYY Account Amt Dr/Cr ...")
    date_str = tokens[0]
    date = parse_date(date_str)
    entries = []
    i = 1
    while i < len(tokens):
        if i + 2 >= len(tokens):
            raise ValueError(f"Incomplete entry at position {i}: need Account Amount Dr/Cr")
        account = tokens[i]
        try:
            amount = Decimal(str(tokens[i + 1]))
        except Exception:
            raise ValueError(f"'{tokens[i+1]}' is not a valid amount")
        dr_cr = tokens[i + 2].lower()
        if dr_cr in ("dr", "debit"):
            entry_type = "debit"
        elif dr_cr in ("cr", "credit"):
            entry_type = "credit"
        else:
            raise ValueError(f"'{tokens[i+2]}' must be Dr or Cr")
        entries.append(Entry(account, amount, entry_type))
        i += 3
    if len(entries) < 2:
        raise ValueError("Need at least 2 entries")
    has_dr = any(e.entry_type == "debit" for e in entries)
    has_cr = any(e.entry_type == "credit" for e in entries)
    if not has_dr or not has_cr:
        raise ValueError("Need both Dr and Cr entries")
    total_dr = sum(e.amount for e in entries if e.entry_type == "debit")
    total_cr = sum(e.amount for e in entries if e.entry_type == "credit")
    if total_dr != total_cr:
        raise ValueError(f"Debits ({total_dr}) do not equal Credits ({total_cr})")
    return date, description, entries

def main():
    storage = Storage()
    engine = LedgerEngine(storage)
    reports = ReportGenerator(engine)
    print("LEDGER CLI - Double-Entry Accounting System")
    print("Type 'help' for commands\n")
    while True:
        try:
            user_input = input("ledger> ").strip()
            if not user_input:
                continue
            cmd = user_input.lower().split()[0] if user_input.split() else ""
            if cmd == "exit":
                print("Goodbye!")
                break
            if cmd == "help":
                print_help()
                continue
            if cmd == "list":
                transactions = engine.get_transactions()
                if not transactions:
                    print("No transactions found.")
                else:
                    print("\nALL TRANSACTIONS")
                    print("-" * 70)
                    for tx in transactions:
                        print(f"{tx.id} | {tx.date} | {tx.description}")
                        for entry in tx.entries:
                            print(f"    {entry.account}: {entry.amount:.2f} {entry.entry_type}")
                        print()
                continue
            if cmd == "trial":
                print(reports.trial_balance())
                continue
            if cmd == "ledger":
                print(reports.ledger())
                continue
            if cmd == "balance":
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print("Usage: balance <account_name>")
                else:
                    account = parts[1].strip().strip('"')
                    balance = engine.get_account_balance(account)
                    print(f"\n{account}: {balance:.2f}\n")
                continue
            if cmd == "delete":
                parts = user_input.split()
                if len(parts) < 2:
                    print("Usage: delete <transaction_id>")
                else:
                    tx_id = parts[1]
                    if engine.delete_transaction(tx_id):
                        print(f"Transaction {tx_id} deleted.")
                    else:
                        print(f"Transaction {tx_id} not found.")
                continue
            if cmd == "add":
                rest = user_input[4:].strip()
                try:
                    date, description, entries = parse_add_command(rest)
                    tx = engine.add_transaction(date, description, entries)
                    print("Transaction added successfully!")
                    print(f"   ID: {tx.id}")
                    print(f"   Date: {tx.date}")
                    print(f"   Description: {tx.description}")
                    for e in tx.entries:
                        print(f"   {e.account}: {e.amount:.2f} {e.entry_type}")
                except ValueError as e:
                    print(f"Error: {e}")
                continue
            print(f"Unknown command '{cmd}'. Type 'help' for available commands.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()