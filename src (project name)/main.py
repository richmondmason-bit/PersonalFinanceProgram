import pygame
from datetime import date
import helper
import budget_goal

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Finance Tracker")

font = pygame.font.SysFont("consolas", 20)

transactions = helper.load_transactions()
settings = budget_goal.load_settings()

state = "menu"
user_text = ""
history = []

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
                        state = "income"
                    elif cmd == "2":
                        state = "expense"
                    elif cmd == "3":
                        income, expense, net = helper.calculate_balance(transactions)
                        goal = settings.get("goal", 0)
                        progress = budget_goal.goal_progress(net, goal)
                        history.append(f"Income: ${income:.2f} Expense: ${expense:.2f} Net: ${net:.2f}")
                        history.append(f"Goal Progress: {progress:.1f}%")
                    elif cmd == "4":
                        state = "budget"
                    elif cmd == "5":
                        state = "goal"
                    elif cmd == "6":
                        pie = helper.create_pie(transactions)
                        if pie:
                            screen.blit(pie, (200,150))
                            pygame.display.flip()
                            pygame.time.delay(2000)
                    elif cmd == "7":
                        running = False

                elif state in ["income","expense"]:
                    try:
                        amt = float(cmd)
                        transactions.append({
                            "date": date.today().isoformat(),
                            "type": "income" if state=="income" else "expense",
                            "amount": amt,
                            "detail": "General"
                        })
                        helper.save_transactions(transactions)
                        history.append("Saved!")
                        state = "menu"
                    except:
                        history.append("Invalid amount")

                elif state == "goal":
                    try:
                        budget_goal.set_goal(settings, float(cmd))
                        budget_goal.save_settings(settings)
                        history.append("Goal updated")
                        state = "menu"
                    except:
                        history.append("Invalid number")

                elif state == "budget":
                    try:
                        cat, amt = cmd.split(",")
                        budget_goal.set_budget(settings, cat.strip(), float(amt))
                        budget_goal.save_settings(settings)
                        history.append("Budget set")
                        state = "menu"
                    except:
                        history.append("Use format: Food,300")

            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    # UI
    draw_text("1:Add Income  2:Add Expense  3:View Balance", 20)
    draw_text("4:Set Budget (Food,300)  5:Set Goal", 50)
    draw_text("6:Pie Chart  7:Quit", 80)

    y = 120
    for h in history[-10:]:
        draw_text(h, y)
        y += 25

    draw_text("> " + user_text, 520)

    pygame.display.flip()

pygame.quit()