import tkinter as tk
from tkinter import messagebox
import helper
import budget_goal
from datetime import datetime

class BudgetWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("280x350")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#ffffff")
        self.root.resizable(True, True)  # allows growth if many categories

        # UI Header
        tk.Label(root, text="BUDGET STATUS", bg="#ffffff", fg="#888888", 
                 font=("Helvetica", 8, "bold")).pack(pady=(15, 5))

        # Scrollable Status Area
        self.status_frame = tk.Frame(root, bg="#ffffff")
        self.status_frame.pack(fill="both", expand=True, padx=20)
        
        self.update_status_view()

        # Auto-refresh every 3 seconds so widget stays live when main app changes data
        self.root.after(3000, self.refresh)

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

    def refresh(self):
        self.update_status_view()
        self.root.after(3000, self.refresh)

    def update_status_view(self):
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        settings = budget_goal.load_settings()
        expenses = helper.load_expenses()
        totals = helper.category_totals(expenses)
        budgets = budget_goal.all_budgets(settings)
        
        if not budgets:
            tk.Label(self.status_frame, text="No budgets set", bg="#ffffff", 
                     fg="#bbbbbb", font=("Helvetica", 9, "italic")).pack(pady=20)
            return

        for cat, limit in budgets.items():
            spent = totals.get(cat, 0.0)
            color = "#e74c3c" if spent > limit else "#2ecc71"
            remaining = limit - spent
            
            row = tk.Frame(self.status_frame, bg="#ffffff")
            row.pack(fill="x", pady=2)
            
            tk.Label(row, text=cat.upper(), bg="#ffffff", font=("Helvetica", 9, "bold")).pack(side=tk.LEFT)
            tk.Label(row, text=f"${spent:.0f} / ${limit:.0f} ({remaining:.0f} left)", 
                     bg="#ffffff", fg=color, font=("Helvetica", 9)).pack(side=tk.RIGHT)

    def set_budget(self):
        cat = self.entry_cat.get().strip()
        if not cat:
            messagebox.showerror("Error", "Enter a category name")
            return
        try:
            limit = float(self.entry_amt.get())
            if limit <= 0:
                raise ValueError
            settings = budget_goal.load_settings()
            budget_goal.set_budget(settings, cat, limit)
            budget_goal.save_settings(settings)
            self.update_status_view()
        except ValueError:
            messagebox.showerror("Error", "Enter a positive amount")

    def add_expense(self):
        cat = self.entry_cat.get().strip()
        if not cat:
            messagebox.showerror("Error", "Enter a category name")
            return
        try:
            amount = float(self.entry_amt.get())
            if amount <= 0:
                raise ValueError
            expense_data = helper.load_expenses()
            expense_data.append({
                "date": datetime.now().isoformat(),
                "amount": amount,
                "category": cat
            })
            helper.save_expenses(expense_data)
            self.update_status_view()
        except ValueError:
            messagebox.showerror("Error", "Enter a positive amount")

    def placeholder_text(self, entry, text):
        entry.insert(0, text)
        entry.bind("<FocusIn>", lambda e: entry.delete('0', 'end') if entry.get() == text else None)

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetWidget(root)
    root.mainloop()