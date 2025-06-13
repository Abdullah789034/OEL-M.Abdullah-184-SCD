from datetime import datetime
import sqlite3

class Transaction:
    """Represents a financial transaction (income or expense)."""
    def __init__(self, id=None, trans_type="income", amount=0.0, category="General", date=None, description=""):
        self.id = id
        self.type = trans_type
        self.amount = float(amount)
        self.category = category
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.description = description

    def validate(self):
        """Validate transaction data."""
        if not isinstance(self.amount, (int, float)) or self.amount <= 0:
            raise ValueError("Amount must be a positive number.")
        if self.type not in ["income", "expense"]:
            raise ValueError("Type must be 'income' or 'expense'.")
        if not self.category:
            raise ValueError("Category cannot be empty.")
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

class CategoryManager:
    """Manages transaction categories."""
    def __init__(self):
        self.categories = ["Food", "Travel", "Utilities", "Salary", "General"]

    def get_categories(self):
        """Return list of available categories."""
        return self.categories

    def add_category(self, category):
        """Add a new category if it doesn't exist."""
        if category and category not in self.categories:
            self.categories.append(category)
            return True
        return False

class Budget:
    """Manages monthly budget and tracks spending."""
    def __init__(self, category, limit):
        self.category = category
        self.limit = float(limit)
        self.spent = 0.0  # Explicitly initialize spent

    def update_spent(self, amount):
        """Update spent amount and check for overflow."""
        self.spent += float(amount)
        if self.spent > self.limit:
            return False  # Budget exceeded
        return True

    def reset(self):
        """Reset spent amount for new period."""
        self.spent = 0.0