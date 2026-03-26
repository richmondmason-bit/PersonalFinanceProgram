import pygame
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)
PROMPT_COLOR = (0, 255, 100)
HISTORY_COLOR = (120, 120, 120)
ERROR_COLOR = (255, 80, 80)
SUCCESS_COLOR = (0, 255, 0)

CHARACTER_LIMIT = 30
MAX_HISTORY = 20

SAVE_FILE = Path("transactions.json")

class Transaction:
    def __init__(self, name: str, amount: float):
        self.name = name.strip()
        self.amount = amount  # positive = income, negative = expense

    def __str__(self):
        sign = "+" if self.amount >= 0 else ""
        return f"{self.name}: {sign}${self.amount:.2f}"

def load_transactions() -> List[Dict]:
    if SAVE_FILE.exists():
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not load saved transactions.")
    return []

def save_transactions(transactions: List[Dict]):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(transactions, f, indent=2)
    except IOError:
        print("Warning: Could not save transactions.")

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Finance Tracker")
    font = pygame.font.SysFont("consolas", 18)
    small_font = pygame.font.SysFont("consolas", 16)

    image_path = Path("testing/Pictures/1615991837602.png")
    try:
        logo = pygame.image.load(image_path).convert_alpha()
        logo = pygame.transform.scale(logo, (426, 240))
    except (pygame.error, FileNotFoundError):
        print(f"Could not load image: {image_path}")
        logo = None

  
    transactions: List[Dict] = load_transactions()

    state = "MENU"
    history: List[str] = ["Welcome to Finance Tracker.", 
                          "[1] Add Transaction", 
                          "[2] View Total",
                          "[3] View All Transactions",
                          "[Q] Quit"]
    
    current_entry: Dict[str, any] = {}
    user_text = ""
    running = True
    clock = pygame.time.Clock()

    while running:
    
        if state == "MENU":
            active_question = "SELECT (1-3 or Q):"
        elif state == "GET_NAME":
            active_question = "ENTER ITEM NAME:"
        elif state == "GET_AMOUNT":
            name = current_entry.get('name', '')
            active_question = f"AMOUNT FOR '{name}' (use - for expense):"
        elif state == "CONFIRM":
            name = current_entry.get('name', '')
            amt = current_entry.get('amount', 0)
            active_question = f"SAVE '{name}' (${amt:.2f})? (y/n):"
        else:
            active_question = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    cmd = user_text.strip()
                    history.append(f"{active_question} {user_text}")

                    if len(user_text) > CHARACTER_LIMIT:
                        history.append("Error: Input too long!")
                        user_text = ""
                        continue

                    if state == "MENU":
                        cmd_lower = cmd.lower()
                        if cmd_lower == "1":
                            state = "GET_NAME"
                            current_entry = {}
                        elif cmd_lower == "2":
                            total = sum(t.get('amount', 0) for t in transactions)
                            history.append(f"TOTAL BALANCE: ${total:.2f}")
                            history.append("---")
                        elif cmd_lower == "3":
                            if transactions:
                                history.append("TRANSACTIONS:")
                                for t in transactions[-10:]:  # show last 10
                                    history.append(f"  • {t['name']}: ${t['amount']:.2f}")
                            else:
                                history.append("No transactions yet.")
                        elif cmd_lower == "q":
                            running = False
                        else:
                            history.append("Invalid option. Use 1, 2, 3, or Q.")

                    elif state == "GET_NAME":
                        if cmd:
                            current_entry['name'] = cmd
                            state = "GET_AMOUNT"
                        else:
                            history.append("Error: Name cannot be empty.")

                    elif state == "GET_AMOUNT":
                        try:
                            amount = float(cmd)
                            current_entry['amount'] = amount
                            state = "CONFIRM"
                        except ValueError:
                            history.append("Error: Please enter a valid number (e.g., 45.50 or -12.99).")

                    elif state == "CONFIRM":
                        if cmd.lower() == "y":
                            transactions.append(current_entry.copy())
                            save_transactions(transactions)
                            history.append("✓ TRANSACTION SAVED.")
                        else:
                            history.append("Transaction cancelled.")
                        state = "MENU"
                        current_entry = {}

                    
                    if len(history) > MAX_HISTORY:
                        history = history[-MAX_HISTORY:]

                    user_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    if state != "MENU":
                        state = "MENU"
                        current_entry = {}
                        history.append("Action cancelled.")
                    else:
                        running = False
                else:
                    if event.unicode.isprintable() and len(user_text) < CHARACTER_LIMIT:
                        user_text += event.unicode

        screen.fill(BG_COLOR)

        
        if logo:
            screen.blit(logo, (187, 20))  

        
        y_pos = 280
        for line in history:
            if "Error" in line or "Invalid" in line:
                color = ERROR_COLOR
            elif "SAVED" in line or "TOTAL" in line or "✓" in line:
                color = SUCCESS_COLOR
            else:
                color = HISTORY_COLOR

            surf = font.render(line, True, color)
            screen.blit(surf, (20, y_pos))
            y_pos += 24
            if y_pos > HEIGHT - 100:
                break
        prompt_surf = font.render(active_question, True, PROMPT_COLOR)
        screen.blit(prompt_surf, (20, y_pos))

  
        input_surf = font.render(f"> {user_text}", True, TEXT_COLOR)
        screen.blit(input_surf, (20, y_pos + 28))

    
        status = f"Transactions: {len(transactions)} | State: {state}"
        status_surf = small_font.render(status, True, (100, 100, 100))
        screen.blit(status_surf, (20, HEIGHT - 25))

        pygame.display.flip()
        clock.tick(60)

    save_transactions(transactions)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()