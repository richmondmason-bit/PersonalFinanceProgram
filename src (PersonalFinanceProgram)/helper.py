import csv
from pathlib import Path
from typing import List, Dict
from collections import defaultdict
import matplotlib.pyplot as plt
import io
import pygame

DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

INCOME_FILE = DOCS_DIR / "income.csv"
EXPENSE_FILE = DOCS_DIR / "Expenses.csv"


def load_csv(file_path) -> List[Dict]:
    data = []
    if file_path.exists():
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row["amount"] = float(row["amount"])
                    data.append(row)
                except (ValueError, KeyError):
                    continue
    return data


def load_income():
    data = load_csv(INCOME_FILE)
    # Safe filter: keep only rows with valid source AND not metadata
    return [row for row in data if row.get("source") not in (None, "", " ") and row.get("date") != "METADATA"]


def load_expenses():
    data = load_csv(EXPENSE_FILE)
    # Safe filter: keep only rows with valid category AND not metadata
    return [row for row in data if row.get("category") not in (None, "", " ") and row.get("date") != "METADATA"]


def save_csv(file_path, data, fields):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def save_income(data):
    metadata_rows = []
    if INCOME_FILE.exists():
        with open(INCOME_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("date") == "METADATA":
                    metadata_rows.append(row)
    all_data = data + metadata_rows
    save_csv(INCOME_FILE, all_data, ["date", "amount", "source"])


def save_expenses(data):
    metadata_rows = []
    if EXPENSE_FILE.exists():
        with open(EXPENSE_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("date") == "METADATA":
                    metadata_rows.append(row)
    all_data = data + metadata_rows
    save_csv(EXPENSE_FILE, all_data, ["date", "amount", "category"])


def total_income(data):
    return sum(d["amount"] for d in data)

def total_expenses(data):
    return sum(d["amount"] for d in data)


def category_totals(expenses):
    totals = defaultdict(float)
    for e in expenses:
        cat = e.get("category")
        if not cat:
            continue
        totals[cat] += e["amount"]
    return totals


def create_pie(expenses):
    data = category_totals(expenses)
    if not data:
        return None

    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sorted_data.values(), labels=sorted_data.keys(), autopct="%1.1f%%")
    ax.set_title("Expenses by Category")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    return pygame.image.load(buf, "chart.png")


# === Metadata storage (goal + budgets) – embedded in the two CSVs only ===
def load_goal():
    goal = 0.0
    if INCOME_FILE.exists():
        with open(INCOME_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("date") == "METADATA" and row.get("source") == "GOAL":
                    try:
                        goal = float(row["amount"])
                    except (ValueError, KeyError):
                        pass
    return goal


def load_budgets():
    budgets = {}
    if EXPENSE_FILE.exists():
        with open(EXPENSE_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cat = row.get("category", "")
                if cat.startswith("BUDGET_"):
                    cat_name = cat[7:]
                    try:
                        budgets[cat_name] = float(row["amount"])
                    except (ValueError, KeyError):
                        pass
    return budgets


def save_goal(goal):
    transactions = load_income()
    metadata_rows = [{
        "date": "METADATA",
        "amount": goal,
        "source": "GOAL"
    }]
    all_data = transactions + metadata_rows
    save_csv(INCOME_FILE, all_data, ["date", "amount", "source"])


def save_budgets(budgets):
    transactions = load_expenses()
    metadata_rows = []
    for cat, amt in budgets.items():
        metadata_rows.append({
            "date": "METADATA",
            "amount": amt,
            "category": f"BUDGET_{cat}"
        })
    all_data = transactions + metadata_rows
    save_csv(EXPENSE_FILE, all_data, ["date", "amount", "category"])