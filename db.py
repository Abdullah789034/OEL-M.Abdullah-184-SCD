import sqlite3
from logic import Transaction

class DatabaseHandler:
    """Handles SQLite database operations."""
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        """Initialize database and create tables."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        date TEXT NOT NULL,
                        description TEXT
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS budgets (
                        category TEXT PRIMARY KEY,
                        budget_limit REAL NOT NULL,
                        spent REAL DEFAULT 0.0
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database initialization failed: {e}")

    def add_transaction(self, transaction):
        """Add a transaction to the database."""
        try:
            transaction.validate()
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO transactions (type, amount, category, date, description)
                    VALUES (?, ?, ?, ?, ?)
                """, (transaction.type, transaction.amount, transaction.category, transaction.date, transaction.description))
                conn.commit()
                return cursor.lastrowid
        except (sqlite3.Error, ValueError) as e:
            raise Exception(f"Failed to add transaction: {e}")

    def get_transactions(self):
        """Retrieve all transactions."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM transactions")
                rows = cursor.fetchall()
                return [Transaction(id=row[0], trans_type=row[1], amount=row[2], category=row[3], date=row[4], description=row[5]) for row in rows]
        except sqlite3.Error as e:
            raise Exception(f"Failed to retrieve transactions: {e}")

    def update_transaction(self, transaction):
        """Update an existing transaction."""
        try:
            transaction.validate()
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE transactions
                    SET type = ?, amount = ?, category = ?, date = ?, description = ?
                    WHERE id = ?
                """, (transaction.type, transaction.amount, transaction.category, transaction.date, transaction.description, transaction.id))
                conn.commit()
        except (sqlite3.Error, ValueError) as e:
            raise Exception(f"Failed to update transaction: {e}")

    def delete_transaction(self, transaction_id):
        """Delete a transaction by ID."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to delete transaction: {e}")

    def set_budget(self, budget):
        """Set or update budget for a category."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO budgets (category, budget_limit, spent)
                    VALUES (?, ?, ?)
                """, (budget.category, budget.limit, budget.spent))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to set budget: {e}")

    def get_budget(self, category):
        """Retrieve budget for a category."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT budget_limit, spent FROM budgets WHERE category = ?", (category,))
                row = cursor.fetchone()
                if row:
                    budget = Budget(category, row[0])
                    budget.spent = row[1]  # Set spent amount
                    return budget
                return None
        except sqlite3.Error as e:
            raise Exception(f"Failed to retrieve budget: {e}")