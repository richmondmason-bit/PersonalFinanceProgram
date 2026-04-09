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
    # Safe filter: keep only rows with valid source
    return [row for row in data if row.get("source") not in (None, "", " ")]


def load_expenses():
    data = load_csv(EXPENSE_FILE)
    # Safe filter: keep only rows with valid category (prevents all KeyErrors)
    return [row for row in data if row.get("category") not in (None, "", " ")]


def save_csv(file_path, data, fields):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def save_income(data):
    save_csv(INCOME_FILE, data, ["date", "amount", "source"])


def save_expenses(data):
    save_csv(EXPENSE_FILE, data, ["date", "amount", "category"])


def total_income(data):
    return sum(d["amount"] for d in data)

def total_expenses(data):
    return sum(d["amount"] for d in data)


def category_totals(expenses):
    totals = defaultdict(float)
    for e in expenses:
        cat = e.get("category")
        if not cat:  # safety net even if filter missed something
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