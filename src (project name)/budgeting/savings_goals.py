# SAVINGS GOAL TRACKER PSEUDOCODE
import csv
import os
SAVINGS_FILE = "saving_data.csv"

def load_savings_data():
    if not os.path.exists(SAVINGS_FILE):
        return 0.0, 0.0
    with open(SAVINGS_FILE, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        return float(data[0][0]), float(data[0][1])

def save_savings_data(goal, saved):
    with open(SAVINGS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([goal, saved])

def set_savings_goal():
    try:
        amount = float(input("Enter your savings goal: "))
        if amount > 0:
            _, saved = load_savings_data()
            save_savings_data(amount, saved)
            print("Goal updated!")
        else:
            print("Error: Goal must be greater than 0.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def add_savings():
    goal, saved = load_savings_data()
    try:
        amount = float(input("How much are you adding? "))
        saved += amount
        save_savings_data(goal, saved)
        print(f"New total saved: ${saved:.2f}")
    except ValueError:
        print("Invalid input.")

def view_progress():
    goal, saved = load_savings_data()
    if goal == 0:
        print("No goal set yet.")
        return
    
    percent = (saved / goal) * 100
    print(f"\nGoal: ${goal:.2f} | Saved: ${saved:.2f}")
    print(f"Progress: {percent:.1f}%")
    if saved >= goal:
        print("Congratulations! You've reached your goal!")
