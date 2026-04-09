import tkinter as tk
from tkinter import messagebox
import csv
import os

SAVINGS_FILE = "saving_data.csv"

class SavingsWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Savings")
        
        # --- SIMPLE STYLING ---
        self.root.geometry("300x250") # Compact size
        self.root.config(bg="white")  # Clean background
        self.root.attributes("-topmost", True)
        
        self.goal, self.saved = self.load_data()

        # UI Elements (Simplified padding and fonts)
        tk.Label(root, text="SAVINGS", font=("Arial", 10, "bold"), bg="white", fg="#888").pack(pady=(20, 5))
        
        self.progress_label = tk.Label(root, text=self.get_status_text(), font=("Arial", 14), bg="white")
        self.progress_label.pack(pady=10)

        # Flat entry field
        self.entry = tk.Entry(root, justify='center', font=("Arial", 12), bd=0, highlightthickness=1, highlightbackground="#ddd")
        self.entry.pack(pady=10, ipady=5)
        self.entry.insert(0, "0.00")

        btn_frame = tk.Frame(root, bg="white")
        btn_frame.pack(pady=20)

        # Minimalist buttons
        tk.Button(btn_frame, text="+ Add", command=self.add_savings, relief="flat", bg="#eee", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Set Goal", command=self.set_goal, relief="flat", bg="#eee", width=10).pack(side=tk.LEFT, padx=5)

    def load_data(self):
        if not os.path.exists(SAVINGS_FILE):
            return 0.0, 0.0
        try:
            with open(SAVINGS_FILE, "r") as f:
                data = list(csv.reader(f))
                return float(data[0][0]), float(data[0][1])
        except (IndexError, ValueError, FileNotFoundError):
            return 0.0, 0.0

    def save_data(self):
        with open(SAVINGS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.goal, self.saved])
        self.update_ui()

    def get_status_text(self):
        if self.goal <= 0:
            return "$0.00 / $0.00"
        return f"${self.saved:,.0f} / ${self.goal:,.0f}"

    def update_ui(self):
        self.progress_label.config(text=self.get_status_text())
        if self.saved >= self.goal > 0:
            messagebox.showinfo("Goal Reached!", "You hit your target!")

    def add_savings(self):
        try:
            amount = float(self.entry.get())
            self.saved += amount
            self.save_data()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")

    def set_goal(self):
        try:
            amount = float(self.entry.get())
            if amount > 0:
                self.goal = amount
                self.save_data()
            else:
                messagebox.showwarning("Warning", "Goal must be > 0")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")

if __name__ == "__main__":
    root = tk.Tk()
    app = SavingsWidget(root)
    root.mainloop()