from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from decimal import Decimal
import uuid

@dataclass
class Entry:
    account: str
    amount: Decimal
    entry_type: str  # 'debit' or 'credit'

    def __post_init__(self):
        # Convert float/string to Decimal if needed
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))
        
        # Validate amount is positive
        if self.amount <= 0:
            raise ValueError(f"Amount must be positive, got {self.amount}")
        
        normalized = self.entry_type.strip().lower()
        if normalized in ('dr', 'debit'):
            self.entry_type = 'debit'
        elif normalized in ('cr', 'credit'):
            self.entry_type = 'credit'
        else:
            raise ValueError(f"Invalid entry_type '{self.entry_type}'. Use Dr or Cr.")

@dataclass
class Transaction:
    date: str
    description: str
    entries: List[Entry]
    id: str = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())[:8]
    
    def is_balanced(self) -> bool:
        debits = sum(e.amount for e in self.entries if e.entry_type == 'debit')
        credits = sum(e.amount for e in self.entries if e.entry_type == 'credit')
        return debits == credits  # Decimal compares exactly
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'date': self.date,
            'description': self.description,
            'entries': [
                {'account': e.account, 'amount': str(e.amount), 'type': e.entry_type}
                for e in self.entries
            ]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        entries = [
            Entry(e['account'], e['amount'], e['type'])
            for e in data['entries']
        ]
        return cls(
            id=data['id'],
            date=data['date'],
            description=data['description'],
            entries=entries
        )
