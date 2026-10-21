"""Personal Expense Tracker with CSV
InternCircle Project 03 | Python Programming

Time Complexity:
    - Add Expense: O(1) single-line append operation to CSV file
    - View All Expenses: O(E) where E is total number of recorded expenses
    - Filter Expenses: O(E) single linear scan through rows
    - Category & Total Summaries: O(E) single-pass aggregation
    - Biggest Expense: O(E) single-pass comparison

Space Complexity:
    - Auxiliary Space: O(1) for appending; O(C) for category totals dictionary
      where C is distinct category count (fixed, C <= 10).
"""

import csv
import os
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple

FILE_NAME = os.path.join(os.path.dirname(__file__), "expenses.csv")
FIELDS = ["date", "category", "description", "amount"]
CATEGORIES = ["Food", "Travel", "Study", "Bills", "Fun", "Other"]


# ==============================================================================
# STORAGE HELPERS
# ==============================================================================

def init_file(filepath: str = FILE_NAME) -> None:
    """Creates the CSV file with the standard header row if it does not exist."""
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def save_expense(row: Dict[str, str], filepath: str = FILE_NAME) -> None:
    """Appends a validated expense entry to the CSV file in O(1) time.
    
    Uses newline='' and utf-8 encoding to guarantee Windows cross-platform safety.
    """
    init_file(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(row)


def load_expenses(filepath: str = FILE_NAME) -> List[Dict[str, str]]:
    """Loads all expense records from the CSV file.
    
    Time Complexity: O(E) where E is the count of recorded expenses
    Space Complexity: O(E) memory for loaded entries
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []


# ==============================================================================
# SUMMARY & ANALYTICS HELPERS
# Time Complexity: O(E) | Space Complexity: O(C) where C is category count
# ==============================================================================

def calculate_summaries(rows: List[Dict[str, str]]) -> Tuple[Dict[str, float], float, Optional[Dict[str, str]]]:
    """Calculates category totals, grand total, and finds the single biggest expense.
    
    Returns:
        (category_totals, grand_total, biggest_expense_dict)
    """
    category_totals = defaultdict(float)
    grand_total = 0.0
    biggest_expense = None
    max_amount = -1.0

    for r in rows:
        try:
            amt = float(r["amount"])
        except (ValueError, KeyError):
            continue

        cat = r.get("category", "Other")
        category_totals[cat] += amt
        grand_total += amt

        if amt > max_amount:
            max_amount = amt
            biggest_expense = r

    return dict(category_totals), grand_total, biggest_expense


# ==============================================================================
# INPUT VALIDATION
# ==============================================================================

def prompt_date() -> str:
    """Prompts for and validates an ISO date (YYYY-MM-DD), defaulting to today."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    while True:
        raw = input(f"Enter date (YYYY-MM-DD) [Press Enter for today: {today_str}]: ").strip()
        if not raw:
            return today_str
        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d")
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD (e.g. 2026-10-15).")


def prompt_category() -> str:
    """Prompts the user to pick from predefined categories or input a custom one."""
    print("Categories:")
    for idx, cat in enumerate(CATEGORIES, start=1):
        print(f"  {idx}) {cat}")

    while True:
        raw = input(f"Select category (1-{len(CATEGORIES)}) or type name: ").strip()
        if not raw:
            print("Category cannot be empty.")
            continue
        if raw.isdigit():
            val = int(raw)
            if 1 <= val <= len(CATEGORIES):
                return CATEGORIES[val - 1]
            print(f"Please enter a number between 1 and {len(CATEGORIES)}.")
            continue
        return raw.capitalize()


def prompt_amount() -> float:
    """Prompts for a numeric amount; rejects non-numbers, negative amounts, and zero."""
    while True:
        raw = input("Enter amount ($): ").strip()
        if not raw:
            print("Amount cannot be empty.")
            continue
        try:
            amt = float(raw)
            if amt <= 0:
                print("Amount must be greater than zero.")
                continue
            return amt
        except ValueError:
            print("Invalid number. Please enter a valid amount (e.g., 25.50).")


# ==============================================================================
# VIEW & DISPLAY FORMATTERS
# ==============================================================================

def print_expense_table(rows: List[Dict[str, str]], title: str = "EXPENSES") -> None:
    """Displays expense rows in a clean, aligned tabular format."""
    print("\n" + "=" * 70)
    print(f"  {title.upper()} ({len(rows)} record{'s' if len(rows) != 1 else ''})")
    print("=" * 70)

    if not rows:
        print("  No expense records found.")
        print("=" * 70)
        return

    print(f"{'#':<4}{'Date':<13}{'Category':<14}{'Amount ($)':>12}   {'Description'}")
    print("-" * 70)
    for idx, r in enumerate(rows, start=1):
        amt_val = float(r.get('amount', 0.0))
        amt_str = f"${amt_val:.2f}"
        print(f"{idx:<4}{r.get('date', ''):<13}{r.get('category', ''):<14}{amt_str:>12}   {r.get('description', '')}")
    print("=" * 70)


# ==============================================================================
# MENU ACTIONS
# ==============================================================================

def action_add_expense() -> None:
    """Handles adding a new validated expense entry."""
    print("\n--- ADD NEW EXPENSE ---")
    date_val = prompt_date()
    category_val = prompt_category()
    
    desc_val = input("Enter description: ").strip()
    if not desc_val:
        desc_val = "Miscellaneous expense"

    amount_val = prompt_amount()

    record = {
        "date": date_val,
        "category": category_val,
        "description": desc_val,
        "amount": f"{amount_val:.2f}"
    }

    save_expense(record)
    print(f"\n Expense recorded successfully! [${amount_val:.2f} for {category_val}]")


def action_view_all() -> None:
    """Displays all saved expenses."""
    rows = load_expenses()
    print_expense_table(rows, "All Recorded Expenses")


def action_filter() -> None:
    """Handles filtering expenses by Category or by Month (YYYY-MM)."""
    rows = load_expenses()
    if not rows:
        print("\nNo expenses found to filter.")
        return

    print("\n--- FILTER EXPENSES ---")
    print("1) Filter by Category")
    print("2) Filter by Month (YYYY-MM)")
    print("3) Return to Menu")

    choice = input("Select filter mode (1-3): ").strip()
    if choice == "1":
        cat_search = input("Enter category to filter by: ").strip().lower()
        filtered = [r for r in rows if r.get("category", "").lower() == cat_search]
        print_expense_table(filtered, f"Category: {cat_search.capitalize()}")
    elif choice == "2":
        month_search = input("Enter month to filter (YYYY-MM, e.g. 2026-10): ").strip()
        filtered = [r for r in rows if r.get("date", "").startswith(month_search)]
        print_expense_table(filtered, f"Month: {month_search}")
    else:
        print("Returning to menu.")


def action_summary() -> None:
    """Displays category totals, grand total, and largest expense."""
    rows = load_expenses()
    if not rows:
        print("\nNo expenses to summarize.")
        return

    cat_totals, grand_total, biggest = calculate_summaries(rows)

    print("\n" + "=" * 50)
    print("            EXPENSE SUMMARY & ANALYTICS")
    print("=" * 50)
    print(f"{'Category':<25}{'Total Spending':>20}")
    print("-" * 50)
    for cat, total in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
        print(f"{cat:<25}{f'${total:.2f}':>20}")
    print("-" * 50)
    print(f"{'GRAND TOTAL':<25}{f'${grand_total:.2f}':>20}")
    print("=" * 50)

    if biggest:
        b_amt = float(biggest.get("amount", 0))
        print(f"🏆 Biggest Single Expense:")
        print(f"   Amount     : ${b_amt:.2f}")
        print(f"   Date       : {biggest.get('date', 'N/A')}")
        print(f"   Category   : {biggest.get('category', 'N/A')}")
        print(f"   Description: {biggest.get('description', 'N/A')}")
        print("=" * 50)


# ==============================================================================
# MAIN APPLICATION LOOP
# ==============================================================================

def main() -> None:
    """Main menu loop that repeats until the user chooses to quit."""
    init_file()
    print("=" * 55)
    print("       PERSONAL EXPENSE TRACKER (CSV STORAGE)")
    print("=" * 55)

    while True:
        print("\n" + "-" * 40)
        print("MENU")
        print("-" * 40)
        print("1) Add Expense")
        print("2) View All Expenses")
        print("3) Filter Expenses")
        print("4) Spending Summary")
        print("5) Quit")
        print("-" * 40)

        try:
            choice = input("Choose an option (1-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting program.")
            break

        if choice == "1":
            action_add_expense()
        elif choice == "2":
            action_view_all()
        elif choice == "3":
            action_filter()
        elif choice == "4":
            action_summary()
        elif choice == "5":
            print("\nThank you for using Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
