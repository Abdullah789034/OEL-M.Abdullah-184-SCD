import unittest
from logic import Transaction, Budget, CategoryManager
from db import DatabaseHandler
from datetime import datetime

class TestFinanceSystem(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.db = DatabaseHandler("test_finance.db")
        self.category_manager = CategoryManager()

    def test_transaction_validation(self):
        """Test transaction input validation."""
        # Valid transaction
        trans = Transaction(trans_type="income", amount=100.0, category="Salary", date="2025-06-13", description="Test")
        self.assertIsNotNone(trans)

        # Invalid amount
        with self.assertRaises(ValueError):
            Transaction(trans_type="income", amount=-10, category="Salary", date="2025-06-13")

        # Invalid type
        with self.assertRaises(ValueError):
            Transaction(trans_type="invalid", amount=100, category="Salary", date="2025-06-13")

        # Invalid date
        with self.assertRaises(ValueError):
            Transaction(trans_type="income", amount=100, category="Salary", date="invalid-date")

    def test_budget_overflow(self):
        """Test budget overflow detection."""
        budget = Budget("Food", 100.0)
        self.assertTrue(budget.update_spent(50.0))  # Within limit
        self.assertFalse(budget.update_spent(60.0))  # Exceeds limit

    def test_database_operations(self):
        """Test database CRUD operations."""
        trans = Transaction(trans_type="income", amount=200.0, category="Salary", date="2025-06-13", description="Test")
        trans_id = self.db.add_transaction(trans)
        self.assertIsNotNone(trans_id)

        transactions = self.db.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].amount, 200.0)

        trans.amount = 300.0
        self.db.update_transaction(trans)
        transactions = self.db.get_transactions()
        self.assertEqual(transactions[0].amount, 300.0)

        self.db.delete_transaction(trans_id)
        transactions = self.db.get_transactions()
        self.assertEqual(len(transactions), 0)

    def test_category_manager(self):
        """Test category management."""
        self.assertTrue(self.category_manager.add_category("Entertainment"))
        self.assertFalse(self.category_manager.add_category("Food"))  # Already exists
        self.assertIn("Entertainment", self.category_manager.get_categories())

if __name__ == "__main__":
    unittest.main()