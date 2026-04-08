import pygame
from datetime import datetime
import helper
import budget_goal

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Finance Tracker")

font = pygame.font.SysFont("consolas", 20)

transactions = helper.load_transactions()
settings = budget_goal.load_settings()

ProgramState = "menu"
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
                Command = user_text.strip()
                user_text = ""

                if ProgramState == "menu":
                    if Command == "1":
                        ProgramState = "income"
                    elif Command == "2":
                        ProgramState = "expense"
                    elif Command == "3":
                        income, expense, net = helper.calculate_balance(transactions)
                        goal = settings.get("goal", 0)
                        progress = budget_goal.goal_progress(net, goal)

                        history.append(f"Income: ${income:.2f} Expense: ${expense:.2f} Net: ${net:.2f}")
                        history.append(f"Goal Progress: {progress:.1f}%")

                    elif Command == "4":
                        ProgramState = "budget"

                    elif Command == "5":
                        ProgramState = "goal"

                    elif Command == "6":
                        pie_chart = helper.create_pie(transactions)

                    elif Command == "7":
                        running = False

                    elif Command == "8":
                        if transactions:
                            transactions.pop()
                            helper.save_transactions(transactions)
                            history.append("Last transaction removed")

                elif ProgramState in ["income","expense"]:
                    try:
                        parts = Command.split(",")
                        amt = float(parts[0])
                        detail = parts[1].strip() if len(parts) > 1 else "General"

                        transactions.append({
                            "date": datetime.now().isoformat(),
                            "type": ProgramState,
                            "amount": amt,
                            "detail": detail
                        })

                        helper.save_transactions(transactions)
                        history.append("Saved!")
                        ProgramState = "menu"

                    except ValueError:
                        history.append("Invalid format. Use: amount or amount,category")

                elif ProgramState == "goal":
                    try:
                        budget_goal.set_goal(settings, float(Command))
                        budget_goal.save_settings(settings)
                        history.append("Goal updated")
                        ProgramState = "menu"
                    except ValueError:
                        history.append("Invalid number")

                elif ProgramState == "budget":
                    try:
                        cat, amt = Command.split(",")
                        budget_goal.set_budget(settings, cat.strip(), float(amt))
                        budget_goal.save_settings(settings)
                        history.append("Budget set")
                        ProgramState = "menu"
                    except ValueError:
                        history.append("Use format: Food,300")

            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    # UI
    draw_text("1:Add Income  2:Add Expense  3:View Balance", 20)
    draw_text("4:Set Budget  5:Set Goal  6:Pie Chart", 50)
    draw_text("7:Quit  8:Undo Last", 80)

    # State prompts
    if ProgramState == "income":
        draw_text("Enter: amount,category (e.g. 1000,Salary)", 480)
    elif ProgramState == "expense":
        draw_text("Enter: amount,category (e.g. 25,Food)", 480)
    elif ProgramState == "goal":
        draw_text("Enter goal amount:", 480)
    elif ProgramState == "budget":
        draw_text("Enter category,amount (e.g. Food,300):", 480)

    # History
    y = 120
    for h in history[-10:]:
        color = (0,255,0) if "Saved" in h else (255,255,255)
        draw_text(h, y, color)
        y += 25

    # Input
    draw_text("> " + user_text, 520)

    # Pie chart (persistent display)
    if pie_chart:
        screen.blit(pie_chart, (200,150))

    pygame.display.flip()

pygame.quit()