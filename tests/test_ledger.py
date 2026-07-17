import unittest
import sys
import os

# Add parent directory to path so we can import ledger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decimal import Decimal
from ledger.models import Entry, Transaction
from ledger.engine import LedgerEngine
from ledger.storage import Storage

class TestEntry(unittest.TestCase):
    def test_entry_type_normalization_dr(self):
        e = Entry("Cash", "100", "Dr")
        self.assertEqual(e.entry_type, "debit")
    
    def test_entry_type_normalization_cr(self):
        e = Entry("Cash", "100", "Cr")
        self.assertEqual(e.entry_type, "credit")
    
    def test_invalid_entry_type(self):
        with self.assertRaises(ValueError):
            Entry("Cash", "100", "invalid")

class TestTransaction(unittest.TestCase):
    def test_balanced_transaction(self):
        tx = Transaction("2026-07-17", "Test", [
            Entry("Cash", "100", "Dr"),
            Entry("Revenue", "100", "Cr")
        ])
        self.assertTrue(tx.is_balanced())
    
    def test_unbalanced_transaction(self):
        tx = Transaction("2026-07-17", "Bad", [
            Entry("Cash", "100", "Dr"),
            Entry("Revenue", "50", "Cr")
        ])
        self.assertFalse(tx.is_balanced())

class TestLedgerEngine(unittest.TestCase):
    def setUp(self):
        # Use a temp file for testing
        self.storage = Storage(filename="data/test_ledger.json")
        self.engine = LedgerEngine(self.storage)
        # Clear any existing test data
        self.engine.transactions = []
        self.engine.save()
    
    def tearDown(self):
        # Clean up test file
        if os.path.exists("data/test_ledger.json"):
            os.remove("data/test_ledger.json")
    
    def test_add_transaction(self):
        tx = self.engine.add_transaction("2026-07-17", "Test", [
            Entry("Cash", "1000", "Dr"),
            Entry("Capital", "1000", "Cr")
        ])
        self.assertEqual(len(self.engine.transactions), 1)
        self.assertEqual(tx.description, "Test")
    
    def test_add_unbalanced_transaction_fails(self):
        with self.assertRaises(ValueError):
            self.engine.add_transaction("2026-07-17", "Bad", [
                Entry("Cash", "1000", "Dr"),
                Entry("Capital", "500", "Cr")
            ])
    
    def test_account_balance(self):
        self.engine.add_transaction("2026-07-17", "Test", [
            Entry("Cash", "1000", "Dr"),
            Entry("Capital", "1000", "Cr")
        ])
        self.assertEqual(self.engine.get_account_balance("Cash"), Decimal("1000"))
        self.assertEqual(self.engine.get_account_balance("Capital"), Decimal("-1000"))
    
    def test_delete_transaction(self):
        tx = self.engine.add_transaction("2026-07-17", "Test", [
            Entry("Cash", "100", "Dr"),
            Entry("Revenue", "100", "Cr")
        ])
        self.assertTrue(self.engine.delete_transaction(tx.id))
        self.assertEqual(len(self.engine.transactions), 0)

if __name__ == "__main__":
    unittest.main()