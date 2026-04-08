# BUDGETING SYSTEM PSEUDOCODE
import csv
import os

BUDGET_FILE = "budget_data.csv"

def load_budget_data():
    budget = {} # Format: { 'Food': [limit, spent] }
    if not os.path.exists(BUDGET_FILE):
        return budget
    with open(BUDGET_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            category, limit, spent = row
            budget[category] = [float(limit), float(spent)]
    return budget

def save_budget_data(budget):
    with open(BUDGET_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        for cat, values in budget.items():
            writer.writerow([cat, values[0], values[1]])

def set_budget():
    budget = load_budget_data()
    cat = input("Category name: ")
    try:
        limit = float(input(f"Limit for {cat}: "))
        if cat in budget:
            budget[cat][0] = limit # Update existing
        else:
            budget[cat] = [limit, 0.0] # Create new
        save_budget_data(budget)
        print(f"Budget for {cat} saved.")
    except ValueError:
        print("Invalid number.")

def add_expense():
    budget = load_budget_data()
    cat = input("Enter category: ")
    if cat in budget:
        try:
            amount = float(input("Expense amount: "))
            budget[cat][1] += amount
            save_budget_data(budget)
            print("Expense added.")
        except ValueError:
            print("Invalid number.")
    else:
        print("Category not found.")

def compare_budget():
    budget = load_budget_data()
    for cat, (limit, spent) in budget.items():
        print(f"\nCategory: {cat}")
        print(f"Limit: ${limit:.2f} | Spent: ${spent:.2f}")
        if spent > limit:
            print(f"WARNING: Over budget by ${spent - limit:.2f}")
        elif spent == limit:
            print("Budget reached exactly.")
        else:
            print(f"Remaining: ${limit - spent:.2f}")

def view_budget_status():
    """Entry point for Option 6: View Budget Status"""
    budget = load_budget_data()
    if not budget:
        print("\nNo budget data found. Please set a budget first.")
        return
    
    print("\n--- Current Budget Status ---")

    compare_budget()

def manage_budget():
    """Entry point for Option 4: Set/Update Category Budget"""
    print("\n--- Manage Budget Categories ---")
    set_budget()
