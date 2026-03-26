import pygame
import sys
import csv
from pathlib import Path
from typing import List, Dict

WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)
PROMPT_COLOR = (0, 255, 100)
HISTORY_COLOR = (120, 120, 120)
ERROR_COLOR = (255, 80, 80)
SUCCESS_COLOR = (0, 255, 0)

CHARACTER_LIMIT = 30000000000
MAX_HISTORY = 20000000

CSV_FILE = Path("docs\Expenses.csv")

def load_transactions() -> List[Dict]:
    transactions = []
    if CSV_FILE.exists():
        try:
            with open(CSV_FILE, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        row['amount'] = float(row['amount'])
                        transactions.append(row)
                    except (ValueError, KeyError):
                        pass
        except Exception:
            pass
    return transactions

def save_transactions(transactions: List[Dict]):
    try:
        with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
            fieldnames = ['name', 'amount']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for t in transactions:
                writer.writerow({'name': t.get('name', ''), 'amount': t.get('amount', 0)})
    except Exception:
        pass

def clean_text(text: str) -> str:
    """Remove null characters and other control characters that crash font.render"""
    if not text:
        return ""
    # Remove null characters and control characters (except tab and newline if needed)
    cleaned = ''.join(c for c in text if c >= ' ' or c in '\t\n')
    return cleaned.strip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Finance Tracker")
    
    font = pygame.font.SysFont("consolas", 18)
    small_font = pygame.font.SysFont("consolas", 16)

    pygame.scrap.init()

    image_path = Path("testing/Pictures/1615991837602.png")
    logo = None
    try:
        logo = pygame.image.load(image_path).convert_alpha()
        logo = pygame.transform.scale(logo, (426, 240))
    except Exception:
        pass

    transactions: List[Dict] = load_transactions()

    state = "MENU"
    history: List[str] = [
        "Welcome to Finance Tracker.",
        "[1] Add Transaction",
        "[2] View Total Balance",
        "[3] View Recent Transactions",
        "[Q] Quit"
    ]
    
    current_entry: Dict[str, any] = {}
    user_text = ""
    running = True
    clock = pygame.time.Clock()
    last_blink = 0
    show_cursor = True

    while running:
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - last_blink > 0.5:
            show_cursor = not show_cursor
            last_blink = current_time

        if state == "MENU":
            active_question = "SELECT OPTION (1, 2, 3 or Q):"
        elif state == "GET_NAME":
            active_question = "ENTER ITEM NAME:"
        elif state == "GET_AMOUNT":
            name = current_entry.get('name', 'ITEM')
            active_question = f"ENTER AMOUNT FOR '{name}' (use - for expense):"
        elif state == "CONFIRM":
            name = current_entry.get('name', '')
            amt = current_entry.get('amount', 0.0)
            active_question = f"SAVE '{name}' (${amt:.2f})? (y/n):"
        else:
            active_question = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Clipboard Support
                if event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                    try:
                        clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                        if clipboard_text:
                            pasted = clipboard_text.decode('utf-8', errors='ignore')
                            pasted = clean_text(pasted)
                            remaining = CHARACTER_LIMIT - len(user_text)
                            if remaining > 0:
                                user_text += pasted[:remaining]
                    except Exception:
                        pass

                elif event.key == pygame.K_c and (event.mod & pygame.KMOD_CTRL):
                    if user_text:
                        try:
                            pygame.scrap.put(pygame.SCRAP_TEXT, user_text.encode('utf-8'))
                        except Exception:
                            pass

                elif event.key == pygame.K_RETURN:
                    cmd = user_text.strip()
                    if not cmd and state == "MENU":
                        continue

                    history.append(f"{active_question} {user_text}")

                    if len(user_text) > CHARACTER_LIMIT:
                        history.append("Error: Input too long!")
                        user_text = ""
                        continue

                    processed = False

                    if state == "MENU":
                        cmd_lower = cmd.lower()
                        if cmd_lower == "1":
                            state = "GET_NAME"
                            current_entry = {}
                            processed = True
                        elif cmd_lower == "2":
                            total = sum(t.get('amount', 0) for t in transactions)
                            history.append(f"TOTAL BALANCE: ${total:.2f}")
                            history.append("─" * 50)
                            processed = True
                        elif cmd_lower == "3":
                            if transactions:
                                history.append("RECENT TRANSACTIONS:")
                                for t in transactions[-10:]:
                                    history.append(f"  • {t.get('name', 'Unknown'):<25} ${t.get('amount', 0):>10.2f}")
                            else:
                                history.append("No transactions recorded yet.")
                            history.append("─" * 50)
                            processed = True
                        elif cmd_lower in ["q", "quit", "exit"]:
                            running = False
                            continue
                        else:
                            history.append("Invalid option. Please use 1, 2, 3, or Q.")

                    elif state == "GET_NAME":
                        if cmd:
                            current_entry['name'] = cmd
                            state = "GET_AMOUNT"
                            processed = True
                        else:
                            history.append("Error: Name cannot be empty.")

                    elif state == "GET_AMOUNT":
                        try:
                            clean_amount = cmd.replace(',', '').strip()
                            amount = float(clean_amount)
                            current_entry['amount'] = amount
                            state = "CONFIRM"
                            processed = True
                        except ValueError:
                            history.append("Error: Please enter a valid number (e.g., 45.50 or -12.99)")

                    elif state == "CONFIRM":
                        if cmd.lower() == "y":
                            transactions.append(current_entry.copy())
                            save_transactions(transactions)
                            history.append("✓ TRANSACTION SAVED SUCCESSFULLY.")
                        else:
                            history.append("Transaction cancelled.")
                        state = "MENU"
                        current_entry = {}
                        processed = True

                    if len(history) > MAX_HISTORY:
                        history = history[-MAX_HISTORY:]

                    user_text = ""

                    if processed:
                        screen.fill(BG_COLOR)
                        if logo:
                            screen.blit(logo, (187, 20))

                        y_pos = 280
                        for line in history:
                            if "Error" in line or "Invalid" in line:
                                color = ERROR_COLOR
                            elif "SAVED" in line or "TOTAL" in line or "✓" in line or "BALANCE" in line:
                                color = SUCCESS_COLOR
                            else:
                                color = HISTORY_COLOR
                            surf = font.render(line, True, color)
                            screen.blit(surf, (20, y_pos))
                            y_pos += 24
                            if y_pos > HEIGHT - 140:
                                break

                        prompt_surf = font.render(active_question, True, PROMPT_COLOR)
                        screen.blit(prompt_surf, (20, y_pos))

                        cursor_text = f"> {user_text}" + ("_" if show_cursor else " ")
                        input_surf = font.render(cursor_text, True, TEXT_COLOR)
                        screen.blit(input_surf, (20, y_pos + 28))

                        status = f"Transactions: {len(transactions)} | State: {state}"
                        status_surf = small_font.render(status, True, (100, 100, 100))
                        screen.blit(status_surf, (20, HEIGHT - 28))

                        help_surf = small_font.render("Ctrl+V = Paste | Ctrl+C = Copy", True, (80, 80, 80))
                        screen.blit(help_surf, (20, HEIGHT - 50))

                        pygame.display.flip()
                        continue

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                elif event.key == pygame.K_ESCAPE:
                    if state != "MENU":
                        state = "MENU"
                        current_entry = {}
                        history.append("← Action cancelled.")
                    else:
                        running = False

                else:
                    if event.unicode.isprintable() and len(user_text) < CHARACTER_LIMIT:
                        user_text += event.unicode

        # Main rendering
        screen.fill(BG_COLOR)

        if logo:
            screen.blit(logo, (187, 20))

        y_pos = 280
        for line in history:
            if "Error" in line or "Invalid" in line:
                color = ERROR_COLOR
            elif "SAVED" in line or "TOTAL" in line or "✓" in line or "BALANCE" in line:
                color = SUCCESS_COLOR
            else:
                color = HISTORY_COLOR

            surf = font.render(line, True, color)
            screen.blit(surf, (20, y_pos))
            y_pos += 24
            if y_pos > HEIGHT - 140:
                break

        prompt_surf = font.render(active_question, True, PROMPT_COLOR)
        screen.blit(prompt_surf, (20, y_pos))

        cursor_text = f"> {user_text}" + ("_" if show_cursor and state != "MENU" else " ")
        input_surf = font.render(cursor_text, True, TEXT_COLOR)
        screen.blit(input_surf, (20, y_pos + 28))

        status = f"Transactions: {len(transactions)} | State: {state}"
        status_surf = small_font.render(status, True, (100, 100, 100))
        screen.blit(status_surf, (20, HEIGHT - 28))

        help_surf = small_font.render("Ctrl+V = Paste | Ctrl+C = Copy", True, (80, 80, 80))
        screen.blit(help_surf, (20, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)

    save_transactions(transactions)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()