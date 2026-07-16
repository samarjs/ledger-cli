#!/usr/bin/env python3
import sys
import os
from datetime import datetime
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
| help                   Display this help menu                                |
| exit                   Exit the application                                  |
+------------------------------------------------------------------------------+
""")

def parse_date(date_str):
    """Convert DD/MM/YYYY to YYYY-MM-DD"""
    try:
        day, month, year = date_str.split('/')
        return f"{year}-{month}-{day}"
    except:
        return date_str

def main():
    storage = Storage()
    engine = LedgerEngine(storage)
    reports = ReportGenerator(engine)
    
    print("LEDGER CLI — Double-Entry Accounting System")
    print("Type 'help' for commands\n")
    
    while True:
        try:
            user_input = input("ledger> ").strip()
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if user_input.lower() == "help":
                print_help()
                continue
            
            if user_input.lower() == "list":
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
            
            if user_input.lower() == "trial":
                print(reports.trial_balance())
                continue
            
            if user_input.lower() == "ledger":
                print(reports.ledger())
                continue
            
            if user_input.lower().startswith("balance"):
                parts = user_input.split()
                if len(parts) < 2:
                    print("Usage: balance <account_name>")
                else:
                    account = " ".join(parts[1:])
                    balance = engine.get_account_balance(account)
                    print(f"\n{account}: {balance:.2f}\n")
                continue
            
            # ADD COMMAND
            if user_input.lower().startswith("add"):
                # Remove "add " from start
                rest = user_input[4:].strip()
                
                # Get description in quotes
                if '"' not in rest:
                    print("Error: Description must be in quotes")
                    continue
                
                start_quote = rest.find('"')
                end_quote = rest.find('"', start_quote + 1)
                
                if end_quote == -1:
                    print("Error: Closing quote not found")
                    continue
                
                description = rest[start_quote + 1:end_quote]
                
                # Get everything after description
                after_desc = rest[end_quote + 1:].strip()
                
                # Split into tokens
                tokens = after_desc.split()
                
                if len(tokens) < 5:
                    print("Error: Not enough arguments")
                    print("Format: add \"Description\" DD/MM/YYYY Account1 Amt1 Dr Account2 Amt2 Cr")
                    continue
                
                # First token is date
                date_str = tokens[0]
                date = parse_date(date_str)
                
                # Now parse the rest: Account Amt Dr/Cr Account Amt Dr/Cr
                entries = []
                i = 1
                while i < len(tokens):
                    if i + 2 >= len(tokens):
                        break
                    
                    account = tokens[i]
                    
                    try:
                        amount = float(tokens[i + 1])
                    except ValueError:
                        print(f"Error: '{tokens[i+1]}' is not a valid number")
                        i += 3
                        continue

                    dr_cr = tokens[i + 2].lower()

                    if dr_cr == "dr":
                        entry_type = "debit"
                    elif dr_cr == "cr":
                        entry_type = "credit"
                    else:
                        print(f"Error: '{dr_cr}' must be 'Dr' or 'Cr'")
                        i += 3
                        continue

                    entries.append(Entry(account, amount, entry_type))
                    i += 3
                
                if len(entries) < 2:
                    print("Error: Need at least 2 entries (one Dr and one Cr)")
                    continue
                
                # Check if we have both Dr and Cr
                has_dr = False
                has_cr = False
                for e in entries:
                    if e.entry_type == 'debit':
                        has_dr = True
                    if e.entry_type == 'credit':
                        has_cr = True
                
                if not has_dr or not has_cr:
                    print("Error: Need both Dr and Cr entries")
                    continue
                
                try:
                    tx = engine.add_transaction(date, description, entries)
                    print(f"✓ Transaction added successfully!")
                    print(f"   ID: {tx.id}")
                    print(f"   Date: {tx.date}")
                    print(f"   Description: {tx.description}")
                    for e in tx.entries:
                        print(f"   {e.account}: {e.amount:.2f} {e.entry_type}")
                except Exception as e:
                    print(f"Error: {e}")
                
                continue
            
            print(f"Unknown command. Type 'help'")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()