import json
import os
from typing import List
from .models import Transaction

class Storage:
    def __init__(self, filename: str = "data/ledger.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    def load(self) -> List[Transaction]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as f:
            data = json.load(f)
            return [Transaction.from_dict(tx) for tx in data]
    
    def save(self, transactions: List[Transaction]):
        with open(self.filename, 'w') as f:
            json.dump([tx.to_dict() for tx in transactions], f, indent=2)