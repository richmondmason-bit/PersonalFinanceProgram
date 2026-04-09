import pygame
from datetime import datetime

import helper
import budget_goal

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Finance Tracker")

font = pygame.font.SysFont("consolas", 20)

income_data = helper.load_income()
expense_data = helper.load_expenses()
settings = budget_goal.load_settings()

state = "menu"
user_text = ""
history = []
pie_chart = None

def draw_text(text, y, color=(255,255,255)):
    screen.blit(font.render(text, True, color), (20, y))

running = True
while running:
    screen.fill((30,30,30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                cmd = user_text.strip()
                user_text = ""

                if state == "menu":
                    if cmd == "1":
                        state = "add_income"
                    elif cmd == "2":
                        state = "add_expense"
                    elif cmd == "3":
                        inc = helper.total_income(income_data)
                        exp = helper.total_expenses(expense_data)

                        history.append(f"Income: ${inc:.2f}")
                        history.append(f"Expenses: ${exp:.2f}")
                        history.append(f"Balance: ${inc-exp:.2f}")

                        warnings = budget_goal.check_budget(expense_data, settings)
                        for w in warnings:
                            history.append(w)

                        goal = budget_goal.get_goal(settings)
                        if goal > 0:
                            balance = inc - exp
                            progress = budget_goal.goal_progress(balance, goal)
                            history.append(f"Goal Progress: {progress:.1f}% (${balance:.2f} / ${goal:.2f})")

                    elif cmd == "4":
                        state = "budget"
                    elif cmd == "5":
                        state = "goal"
                    elif cmd == "6":
                        pie_chart = helper.create_pie(expense_data)
                    elif cmd == "7":
                        running = False

                elif state == "add_income":
                    try:
                        amt, source = cmd.split(",")
                        income_data.append({
                            "date": datetime.now().isoformat(),
                            "amount": float(amt),
                            "source": source.strip()
                        })
                        helper.save_income(income_data)
                        history.append("Income saved")
                        state = "menu"
                    except ValueError:
                        history.append("Use: amount,source")

                elif state == "add_expense":
                    try:
                        amt, cat = cmd.split(",")
                        expense_data.append({
                            "date": datetime.now().isoformat(),
                            "amount": float(amt),
                            "category": cat.strip()
                        })
                        helper.save_expenses(expense_data)
                        history.append("Expense saved")
                        state = "menu"
                    except ValueError:
                        history.append("Use: amount,category")

                elif state == "goal":
                    try:
                        budget_goal.set_goal(settings, float(cmd))
                        budget_goal.save_settings(settings)
                        history.append("Goal updated")
                        state = "menu"
                    except ValueError:
                        history.append("Invalid number")

                elif state == "budget":
                    try:
                        cat, amt = cmd.split(",")
                        budget_goal.set_budget(settings, cat.strip(), float(amt))
                        budget_goal.save_settings(settings)
                        history.append("Budget set")
                        state = "menu"
                    except ValueError:
                        history.append("Use: Food,300")

            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    draw_text("1:Add Income  2:Add Expense  3:View Totals", 20)
    draw_text("4:Set Budget  5:Set Goal  6:Pie Chart", 50)
    draw_text("7:Quit", 80)

    if state == "add_income":
        draw_text("Enter: amount,source (1000,Job)", 500)
    elif state == "add_expense":
        draw_text("Enter: amount,category (50,Food)", 500)
    elif state == "goal":
        draw_text("Enter goal amount:", 500)
    elif state == "budget":
        draw_text("Enter category,amount:", 500)

    y = 120
    for h in history[-10:]:
        draw_text(h, y)
        y += 25

    draw_text("> " + user_text, 550)

    if pie_chart:
        screen.blit(pie_chart, (400, 120))

    pygame.display.flip()

pygame.quit()