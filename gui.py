import tkinter as tk
from tkinter import messagebox, ttk
from logic import Transaction, CategoryManager, Budget
from db import DatabaseHandler

class GUIManager:
    """Manages the Tkinter GUI for the finance system."""
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Management System")
        self.db = DatabaseHandler()
        self.category_manager = CategoryManager()
        self.setup_gui()

    def setup_gui(self):
        """Set up the main GUI layout."""
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        # Transaction Entry
        tk.Label(self.frame, text="Type:").grid(row=0, column=0, sticky="w")
        self.type_var = tk.StringVar(value="income")
        tk.Radiobutton(self.frame, text="Income", variable=self.type_var, value="income").grid(row=0, column=1)
        tk.Radiobutton(self.frame, text="Expense", variable=self.type_var, value="expense").grid(row=0, column=2)

        tk.Label(self.frame, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(self.frame)
        self.amount_entry.grid(row=1, column=1, columnspan=2)

        tk.Label(self.frame, text="Category:").grid(row=2, column=0, sticky="w")
        self.category_combo = ttk.Combobox(self.frame, values=self.category_manager.get_categories())
        self.category_combo.grid(row=2, column=1, columnspan=2)
        self.category_combo.set("General")

        tk.Label(self.frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w")
        self.date_entry = tk.Entry(self.frame)
        self.date_entry.grid(row=3, column=1, columnspan=2)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(self.frame, text="Description:").grid(row=4, column=0, sticky="w")
        self.desc_entry = tk.Entry(self.frame)
        self.desc_entry.grid(row=4, column=1, columnspan=2)

        tk.Button(self.frame, text="Add Transaction", command=self.add_transaction).grid(row=5, column=0, columnspan=3, pady=5)

        # Budget Setting
        tk.Label(self.frame, text="Set Budget - Category:").六年

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from logic import Transaction, CategoryManager, Budget
from db import DatabaseHandler

class GUIManager:
    """Manages the Tkinter GUI for the finance system."""
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Management System")
        self.db = DatabaseHandler()
        self.category_manager = CategoryManager()
        self.setup_gui()

    def setup_gui(self):
        """Set up the main GUI layout."""
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        # Transaction Entry
        tk.Label(self.frame, text="Type:").grid(row=0, column=0, sticky="w")
        self.type_var = tk.StringVar(value="income")
        tk.Radiobutton(self.frame, text="Income", variable=self.type_var, value="income").grid(row=0, column=1)
        tk.Radiobutton(self.frame, text="Expense", variable=self.type_var, value="expense").grid(row=0, column=2)

        tk.Label(self.frame, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(self.frame)
        self.amount_entry.grid(row=1, column=1, columnspan=2)

        tk.Label(self.frame, text="Category:").grid(row=2, column=0, sticky="w")
        self.category_combo = ttk.Combobox(self.frame, values=self.category_manager.get_categories())
        self.category_combo.grid(row=2, column=1, columnspan=2)
        self.category_combo.set("General")

        tk.Label(self.frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w")
        self.date_entry = tk.Entry(self.frame)
        self.date_entry.grid(row=3, column=1, columnspan=2)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        tk.Label(self.frame, text="Description:").grid(row=4, column=0, sticky="w")
        self.desc_entry = tk.Entry(self.frame)
        self.desc_entry.grid(row=4, column=1, columnspan=2)

        tk.Button(self.frame, text="Add Transaction", command=self.add_transaction).grid(row=5, column=0, columnspan=3, pady=5)

        # Budget Setting
        tk.Label(self.frame, text="Set Budget - Category:").grid(row=6, column=0, sticky="w")
        self.budget_category_combo = ttk.Combobox(self.frame, values=self.category_manager.get_categories())
        self.budget_category_combo.grid(row=6, column=1, columnspan=2)
        self.budget_category_combo.set("General")

        tk.Label(self.frame, text="Budget Limit:").grid(row=7, column=0, sticky="w")
        self.budget_limit_entry = tk.Entry(self.frame)
        self.budget_limit_entry.grid(row=7, column=1, columnspan=2)

        tk.Button(self.frame, text="Set Budget", command=self.set_budget).grid(row=8, column=0, columnspan=3, pady=5)

        # Transaction List
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Type", "Amount", "Category", "Date", "Description"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Description", text="Description")
        self.tree.grid(row=9, column=0, columnspan=3, pady=5)
        self.update_transaction_list()

        tk.Button(self.frame, text="Delete Selected", command=self.delete_transaction).grid(row=10, column=0, columnspan=3, pady=5)

        # Summary
        self.summary_label = tk.Label(self.frame, text="Summary: Income: 0 | Expenses: 0 | Savings: 0")
        self.summary_label.grid(row=11, column=0, columnspan=3, pady=5)
        self.update_summary()

    def add_transaction(self):
        """Add a new transaction to the database."""
        try:
            trans = Transaction(
                trans_type=self.type_var.get(),
                amount=float(self.amount_entry.get()),
                category=self.category_combo.get(),
                date=self.date_entry.get(),
                description=self.desc_entry.get()
            )
            trans_id = self.db.add_transaction(trans)
            if trans.type == "expense":
                budget = self.db.get_budget(trans.category)
                if budget:
                    budget.update_spent(trans.amount)
                    self.db.set_budget(budget)
                    if budget.spent > budget.limit:
                        messagebox.showwarning("Budget Warning", f"Budget for {trans.category} exceeded!")
            self.update_transaction_list()
            self.update_summary()
            messagebox.showinfo("Success", "Transaction added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add transaction: {e}")

    def set_budget(self):
        """Set a budget for a category."""
        try:
            category = self.budget_category_combo.get()
            limit = float(self.budget_limit_entry.get())
            if limit <= 0:
                raise ValueError("Budget limit must be positive.")
            budget = Budget(category, limit)
            self.db.set_budget(budget)
            messagebox.showinfo("Success", f"Budget set for {category}!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set budget: {e}")

    def delete_transaction(self):
        """Delete the selected transaction."""
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showerror("Error", "No transaction selected.")
                return
            trans_id = self.tree.item(selected)["values"][0]
            self.db.delete_transaction(trans_id)
            self.update_transaction_list()
            self.update_summary()
            messagebox.showinfo("Success", "Transaction deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete transaction: {e}")

    def update_transaction_list(self):
        """Update the transaction list display."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            transactions = self.db.get_transactions()
            for trans in transactions:
                self.tree.insert("", "end", values=(trans.id, trans.type, trans.amount, trans.category, trans.date, trans.description))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transactions: {e}")

    def update_summary(self):
        """Update the financial summary display."""
        try:
            transactions = self.db.get_transactions()
            income = sum(t.amount for t in transactions if t.type == "income")
            expenses = sum(t.amount for t in transactions if t.type == "expense")
            savings = income - expenses
            self.summary_label.config(text=f"Summary: Income: {income:.2f} | Expenses: {expenses:.2f} | Savings: {savings:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update summary: {e}")