import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

BUDGET_FILE = "budget_data.csv"

class BudgetWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("280x350")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#ffffff")  # Clean White Background

        # State
        self.budget = self.load_data()

        # UI Header
        tk.Label(root, text="BUDGET STATUS", bg="#ffffff", fg="#888888", 
                 font=("Helvetica", 8, "bold")).pack(pady=(15, 5))

        # Scrollable Status Area
        self.status_frame = tk.Frame(root, bg="#ffffff")
        self.status_frame.pack(fill="both", expand=True, padx=20)
        
        self.update_status_view()

        # Input Fields
        input_bg = "#f5f5f5"
        self.entry_cat = tk.Entry(root, bg=input_bg, bd=0, justify="center", font=("Helvetica", 10))
        self.entry_cat.pack(pady=2, ipady=4, padx=40, fill="x")
        self.placeholder_text(self.entry_cat, "Category Name")

        self.entry_amt = tk.Entry(root, bg=input_bg, bd=0, justify="center", font=("Helvetica", 10))
        self.entry_amt.pack(pady=2, ipady=4, padx=40, fill="x")
        self.placeholder_text(self.entry_amt, "Amount (Limit or Expense)")

        # Buttons
        btn_frame = tk.Frame(root, bg="#ffffff")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="SET LIMIT", command=self.set_budget, bg="#eeeeee", 
                  fg="#333333", bd=0, padx=10, font=("Helvetica", 8, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="ADD EXPENSE", command=self.add_expense, bg="#4CAF50", 
                  fg="white", bd=0, padx=10, font=("Helvetica", 8, "bold")).pack(side=tk.LEFT, padx=5)

    def load_data(self):
        budget = {}
        if not os.path.exists(BUDGET_FILE):
            return budget
        try:
            with open(BUDGET_FILE, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        budget[row[0]] = [float(row[1]), float(row[2])]
        except: pass
        return budget

    def save_data(self):
        with open(BUDGET_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for cat, values in self.budget.items():
                writer.writerow([cat, values[0], values[1]])
        self.update_status_view()

    def update_status_view(self):
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        if not self.budget:
            tk.Label(self.status_frame, text="No categories set", bg="#ffffff", 
                     fg="#bbbbbb", font=("Helvetica", 9, "italic")).pack(pady=20)
            return

        for cat, (limit, spent) in self.budget.items():
            color = "#e74c3c" if spent > limit else "#2ecc71"
            remaining = limit - spent
            
            row = tk.Frame(self.status_frame, bg="#ffffff")
            row.pack(fill="x", pady=2)
            
            tk.Label(row, text=cat.upper(), bg="#ffffff", font=("Helvetica", 9, "bold")).pack(side=tk.LEFT)
            tk.Label(row, text=f"${spent:.0f} / ${limit:.0f}", bg="#ffffff", 
                     fg=color, font=("Helvetica", 9)).pack(side=tk.RIGHT)

    def set_budget(self):
        cat = self.entry_cat.get()
        try:
            limit = float(self.entry_amt.get())
            self.budget[cat] = [limit, self.budget.get(cat, [0, 0])[1]]
            self.save_data()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount")

    def add_expense(self):
        cat = self.entry_cat.get()
        if cat in self.budget:
            try:
                amount = float(self.entry_amt.get())
                self.budget[cat][1] += amount
                self.save_data()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid amount")
        else:
            messagebox.showerror("Error", "Category not found")

    def placeholder_text(self, entry, text):
        entry.insert(0, text)
        entry.bind("<FocusIn>", lambda e: entry.delete('0', 'end') if entry.get() == text else None)

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetWidget(root)
    root.mainloop()