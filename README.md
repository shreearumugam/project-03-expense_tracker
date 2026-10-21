# Personal Expense Tracker with CSV

**InternCircle | Project 03: Python Programming**

A persistent, menu-driven command-line expense tracker using Python's built-in `csv` and `datetime` modules.

---

## ⚡ Time & Space Complexity Analysis

| Operation / Feature | Time Complexity | Auxiliary Space Complexity | Analysis |
| :--- | :---: | :---: | :--- |
| **Add Expense (`save_expense`)** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Constant time direct append (`"a"`) to the CSV file. |
| **Load Expenses (`load_expenses`)** | $\mathcal{O}(E)$ | $\mathcal{O}(E)$ | Reads all $E$ rows into memory for viewing/filtering. |
| **Filter by Category / Month** | $\mathcal{O}(E)$ | $\mathcal{O}(K)$ | Single linear pass through rows; $K \le E$ filtered subset. |
| **Spending Summaries & Totals** | $\mathcal{O}(E)$ | $\mathcal{O}(C)$ | Single linear aggregation pass; $C \le 10$ distinct categories. |
| **Find Biggest Expense** | $\mathcal{O}(E)$ | $\mathcal{O}(1)$ | Single linear scan finding the maximum scalar value. |

---

## 📝 Submission Note (One Problem Fixed)

> **Problem Encountered & Fixed**:  
> When working with CSV files on Windows operating systems, opening files in default write/append mode without `newline=""` produces an extraneous carriage return `\r\r\n`, which generates unintended blank lines between every data row in spreadsheet applications (such as Excel or LibreOffice).  
> **Resolution**: Explicitly specified `open(..., newline="", encoding="utf-8")` across all file handlers (`init_file`, `save_expense`, and `load_expenses`), ensuring consistent cross-platform behavior and clean spreadsheet rendering.

---

## 📋 Checklist Verification

- [x] **Data is saved to expenses.csv and reloaded on restart**: Uses persistent append and read operations.
- [x] **Dates and amounts are validated**: Dates must match `YYYY-MM-DD` via `datetime.strptime`; amounts must be positive numbers.
- [x] **You can filter by category and by month**: Filter options allow matching specific categories or substring prefix `YYYY-MM`.
- [x] **The summary shows totals per category and a grand total**: Aggregates totals with dictionary and displays largest expense.
- [x] **The menu is easy to follow**: Clean, numbered options (1-5) with safe inputs.
- [x] **A README explains how to run it**: Step-by-step instructions and complexity details included.

---

## 🚀 How to Run

```bash
# Run the expense tracker
python expense_tracker.py

# Run unit tests
python test_expense_tracker.py
```
