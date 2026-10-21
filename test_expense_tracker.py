"""Unit tests for Project 03: Personal Expense Tracker with CSV."""

import os
import unittest
from expense_tracker import (
    calculate_summaries,
    init_file,
    load_expenses,
    save_expense,
)


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(__file__)
        self.temp_csv = os.path.join(self.test_dir, "temp_test_expenses.csv")
        if os.path.exists(self.temp_csv):
            os.remove(self.temp_csv)
        init_file(self.temp_csv)

    def tearDown(self):
        if os.path.exists(self.temp_csv):
            os.remove(self.temp_csv)

    def test_save_and_load_expenses(self):
        item = {
            "date": "2026-10-15",
            "category": "Food",
            "description": "Lunch meeting",
            "amount": "25.50",
        }
        save_expense(item, self.temp_csv)

        records = load_expenses(self.temp_csv)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["category"], "Food")
        self.assertEqual(float(records[0]["amount"]), 25.50)

    def test_calculate_summaries(self):
        sample_rows = [
            {"date": "2026-10-01", "category": "Food", "description": "Groceries", "amount": "50.00"},
            {"date": "2026-10-05", "category": "Food", "description": "Snacks", "amount": "15.00"},
            {"date": "2026-10-10", "category": "Study", "description": "Book", "amount": "35.00"},
            {"date": "2026-11-01", "category": "Bills", "description": "Internet", "amount": "60.00"},
        ]
        cat_totals, grand_total, biggest = calculate_summaries(sample_rows)

        self.assertEqual(cat_totals["Food"], 65.00)
        self.assertEqual(cat_totals["Study"], 35.00)
        self.assertEqual(cat_totals["Bills"], 60.00)
        self.assertEqual(grand_total, 160.00)
        self.assertIsNotNone(biggest)
        self.assertEqual(biggest["category"], "Bills")
        self.assertEqual(float(biggest["amount"]), 60.00)

    def test_seed_expenses_has_minimum_ten_rows(self):
        seed_csv = os.path.join(self.test_dir, "expenses.csv")
        self.assertTrue(os.path.exists(seed_csv), "expenses.csv must exist")
        records = load_expenses(seed_csv)
        self.assertGreaterEqual(len(records), 10, "expenses.csv must contain at least 10 rows")

        # Verify cross two months
        months = {r["date"][:7] for r in records}
        self.assertGreaterEqual(len(months), 2, "Data must span across at least two months")


if __name__ == "__main__":
    unittest.main()
