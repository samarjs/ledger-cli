from typing import List, Dict, Optional
from .models import Transaction, Entry
from .storage import Storage

class LedgerEngine:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.transactions: List[Transaction] = []
        self.load()
    
    def load(self):
        self.transactions = self.storage.load()
    
    def save(self):
        self.storage.save(self.transactions)
    
    def add_transaction(self, date: str, description: str, entries: List[Entry]) -> Transaction:
        tx = Transaction(date=date, description=description, entries=entries)
        if not tx.is_balanced():
            raise ValueError("Transaction is not balanced! Debits must equal Credits.")
        self.transactions.append(tx)
        self.save()
        return tx
    
    def get_account_balance(self, account: str) -> float:
        balance = 0.0
        for tx in self.transactions:
            for entry in tx.entries:
                if entry.account == account:
                    if entry.entry_type == 'debit':
                        balance += entry.amount
                    else:
                        balance -= entry.amount
        return balance
    
    def get_all_accounts(self) -> List[str]:
        accounts = set()
        for tx in self.transactions:
            for entry in tx.entries:
                accounts.add(entry.account)
        return sorted(list(accounts))
    
    def get_trial_balance(self) -> Dict[str, float]:
        trial_balance = {}
        for account in self.get_all_accounts():
            trial_balance[account] = self.get_account_balance(account)
        return trial_balance
    
    def get_transactions(self) -> List[Transaction]:
        return self.transactions