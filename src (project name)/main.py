import pygame
from datetime import datetime
import subprocess
import os

import helper
import budget_goal

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Finance Tracker")

font = pygame.font.SysFont("consolas", 20)

income_data = helper.load_income()
expense_data = helper.load_expenses()
settings = budget_goal.load_settings()
pie_chart = helper.create_pie(expense_data)

last_refresh = pygame.time.get_ticks()

ProgramState = "menu"
user_text = ""
HISTORY = []

def draw_text(text, y, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), (20, y))

Run = True
while Run:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                Command = user_text.strip()
                user_text = ""

                if ProgramState == "menu":
                    if Command == "1":
                        ProgramState = "add_income"
                    elif Command == "2":
                        ProgramState = "add_expense"
                    elif Command == "3":
                        warnings = budget_goal.check_budget(expense_data, settings)
                        for w in warnings:
                            HISTORY.append(w)
                        if not warnings:
                            HISTORY.append("All budgets on track.")
                    elif Command == "4":
                        ProgramState = "budget"
                    elif Command == "5":
                        ProgramState = "goal"
                    elif Command == "6":
                        pie_chart = helper.create_pie(expense_data)
                    elif Command == "7":
                        Run = False
                    elif Command == "8":
                        income_data = helper.load_income()
                        expense_data = helper.load_expenses()
                        settings = budget_goal.load_settings()
                        pie_chart = helper.create_pie(expense_data)
                        HISTORY.append("Data refreshed from disk")
                    elif Command == "9":
                        widget_path = os.path.join(os.path.dirname(__file__), "budget_widget.py")
                        if os.path.exists(widget_path):
                            try:
                                subprocess.Popen(["python", widget_path])
                                HISTORY.append("Budget widget launched")
                            except Exception as e:
                                HISTORY.append(f"Widget launch failed: {e}")
                        else:
                            HISTORY.append("budget_widget.py not found in folder")

                elif ProgramState == "add_income":
                    try:
                        amt_str, source = Command.split(",", 1)
                        amt = float(amt_str.strip())
                        if amt <= 0:
                            raise ValueError
                        income_data.append({
                            "date": datetime.now().isoformat(),
                            "amount": amt,
                            "source": source.strip()
                        })
                        helper.save_income(income_data)
                        HISTORY.append("Income saved")
                        ProgramState = "menu"
                    except (ValueError, IndexError):
                        HISTORY.append("Use: amount,source (1000,Job) - amount > 0")

                elif ProgramState == "add_expense":
                    try:
                        amt_str, cat = Command.split(",", 1)
                        amt = float(amt_str.strip())
                        if amt <= 0:
                            raise ValueError
                        expense_data.append({
                            "date": datetime.now().isoformat(),
                            "amount": amt,
                            "category": cat.strip()
                        })
                        helper.save_expenses(expense_data)
                        HISTORY.append("Expense saved")
                        pie_chart = helper.create_pie(expense_data)
                        ProgramState = "menu"
                    except (ValueError, IndexError):
                        HISTORY.append("Use: amount,category (50,Food) - amount > 0")

                elif ProgramState == "goal":
                    try:
                        amt = float(Command)
                        if amt <= 0:
                            raise ValueError
                        budget_goal.set_goal(settings, amt)
                        budget_goal.save_settings(settings)
                        HISTORY.append("Goal updated")
                        ProgramState = "menu"
                    except ValueError:
                        HISTORY.append("Goal must be positive number")

                elif ProgramState == "budget":
                    try:
                        cat, amt_str = Command.split(",", 1)
                        amt = float(amt_str.strip())
                        if amt <= 0:
                            raise ValueError
                        budget_goal.set_budget(settings, cat.strip(), amt)
                        budget_goal.save_settings(settings)
                        HISTORY.append("Budget set")
                        ProgramState = "menu"
                    except (ValueError, IndexError):
                        HISTORY.append("Use: category,positive_amount (Food,300)")

            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    # === Auto-refresh every 3 seconds for live sync with widget ===
    current_time = pygame.time.get_ticks()
    if current_time - last_refresh > 3000:
        income_data = helper.load_income()
        expense_data = helper.load_expenses()
        settings = budget_goal.load_settings()
        pie_chart = helper.create_pie(expense_data)
        last_refresh = current_time

    # Menu
    draw_text("1:Add Income  2:Add Expense  3:View Totals  8:Refresh Data", 20)
    draw_text("4:Set Budget  5:Set Goal  6:Pie Chart  9:Launch Widget", 50)
    draw_text("7:Quit", 80)

    # Live summary + goal + budget status (always visible)
    y = 120
    Income = helper.total_income(income_data)
    Exp = helper.total_expenses(expense_data)
    Balance = Income - Exp
    draw_text(f"Income: ${Income:.2f}   Expenses: ${Exp:.2f}   Balance: ${Balance:.2f}", y)
    y += 25

    goal = budget_goal.get_goal(settings)
    if goal > 0:
        Progress = budget_goal.goal_progress(Balance, goal)
        gcolor = (46, 204, 113) if Progress <= 100 else (231, 76, 60)
        draw_text(f"Goal Progress: {Progress:.1f}% (${Balance:.2f} / ${goal:.2f})", y, gcolor)
        y += 25

    budgets_dict = budget_goal.all_budgets(settings)
    if budgets_dict:
        totals = helper.category_totals(expense_data)
        for cat, limit in budgets_dict.items():
            spent = totals.get(cat, 0)
            color = (231, 76, 60) if spent > limit else (46, 204, 113)
            remaining = limit - spent
            btext = f"{cat.upper()}: ${spent:.0f} / ${limit:.0f}  ({remaining:.0f} remaining)"
            screen.blit(font.render(btext, True, color), (20, y))
            y += 25

    # History (subdued color, starts after dynamic status)
    history_y = y + 10
    for h in HISTORY[-10:]:
        draw_text(h, history_y, (180, 180, 180))
        history_y += 25

    # State prompts
    if ProgramState == "add_income":
        draw_text("Enter: amount,source (1000,Job)", 500)
    elif ProgramState == "add_expense":
        draw_text("Enter: amount,category (50,Food)", 500)
    elif ProgramState == "goal":
        draw_text("Enter goal amount:", 500)
    elif ProgramState == "budget":
        draw_text("Enter category,amount:", 500)

    draw_text("> " + user_text, 550)

    if pie_chart:
        screen.blit(pie_chart, (400, 120))

    pygame.display.flip()

pygame.quit()