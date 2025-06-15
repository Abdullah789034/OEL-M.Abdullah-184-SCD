import unittest
from logic import Transaction, Budget, CategoryManager
from db import DatabaseHandler
from datetime import datetime

class TestFinanceSystem(unittest.TestCase):
    def setUp(self):
        """Set up in-memory database and category manager."""
        self.db = DatabaseHandler(":memory:")
        self.db._init_db()  # Initialize tables in DatabaseHandler's database
        self.category_manager = CategoryManager()

    def tearDown(self):
        """No cleanup needed for in-memory database."""
        pass

    def test_transaction_validation(self):
        """Test transaction input validation."""
        trans = Transaction(amount=100.0, category="Salary", date="2025-06-13")
        self.assertEqual(trans.amount, 100.0)
        self.assertEqual(trans.category, "Salary")
        self.assertEqual(trans.date, "2025-06-13")

        tests = [
            ({"amount": -10}, "Amount must be a positive number."),
            ({"amount": 0}, "Amount must be a positive number."),
            ({"trans_type": "invalid"}, "Type must be 'income' or 'expense'."),
            ({"date": "invalid-date"}, "Invalid date format. Use YYYY-MM-DD."),
            ({"category": ""}, "Category cannot be empty.")
        ]
        for kwargs, error in tests:
            try:
                Transaction(**{"amount": 100.0, "category": "Salary", "date": "2025-06-13", **kwargs})
                self.fail(f"Expected ValueError for {kwargs}")
            except ValueError as e:
                self.assertEqual(str(e), error)

    def test_budget_operations(self):
        """Test budget operations."""
        budget = Budget("Food", 100.0)
        self.assertTrue(budget.update_spent(50.0))
        self.assertEqual(budget.spent, 50.0)
        self.assertFalse(budget.update_spent(60.0))
        budget.reset()
        self.assertEqual(budget.spent, 0.0)


    def test_category_manager(self):
        """Test category management."""
        self.assertTrue(self.category_manager.add_category("Entertainment"))
        self.assertFalse(self.category_manager.add_category("Food"))
        self.assertIn("Entertainment", self.category_manager.get_categories())


if __name__ == "__main__":
    unittest.main()