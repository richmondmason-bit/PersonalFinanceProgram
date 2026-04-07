import csv
from pathlib import Path
from typing import List, Dict
from collections import defaultdict
import matplotlib.pyplot as plt
import io
import pygame

CSV_FILE = Path(r"docs\Expenses.csv")

def load_transactions() -> List[Dict]:
    transactions = []
    if CSV_FILE.exists():
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['amount'] = float(row['amount'])
                    transactions.append(row)
                except:
                    pass
    return transactions

def save_transactions(transactions: List[Dict]):
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date","type","amount","detail"])
        writer.writeheader()
        writer.writerows(transactions)

def calculate_balance(transactions):
    income = sum(t['amount'] for t in transactions if t['type']=="income")
    expense = sum(t['amount'] for t in transactions if t['type']=="expense")
    return income, expense, income - expense

def category_totals(transactions):
    totals = defaultdict(float)
    for t in transactions:
        if t['type'] == 'expense':
            totals[t['detail']] += t['amount']
    return totals

def create_pie(transactions):
    data = category_totals(transactions)
    if not data:
        return None

    fig, ax = plt.subplots()
    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return pygame.image.load(buf, 'chart.png')