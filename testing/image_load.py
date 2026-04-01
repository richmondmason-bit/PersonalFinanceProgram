import pygame
import sys
import csv
from pathlib import Path
from typing import List, Dict

WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)
PROMPT_COLOR = (0, 255, 100)
HISTORY_COLOR = (180, 180, 180)
ERROR_COLOR = (255, 80, 80)
SUCCESS_COLOR = (0, 255, 0)
LINE_HEIGHT = 24
VISIBLE_LINES = 18
HISTORY_START_Y = 20
CHARACTER_LIMIT = 300
MAX_HISTORY = 20

CSV_FILE = Path("docs/Expenses.csv")


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
        CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
            fieldnames = ['name', 'amount']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for t in transactions:
                writer.writerow({'name': t.get('name', ''), 'amount': t.get('amount', 0)})
        return True
    except Exception:
        return False


def clean_text(text: str) -> str:
    if not text:
        return ""
    return ''.join(c for c in text if c >= ' ' or c in '\t\n').strip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Finance Tracker")
    
    font = pygame.font.SysFont("consolas", 18)
    small_font = pygame.font.SysFont("consolas", 16)

    pygame.scrap.init()

    logo = None
    try:
        image_path = Path("testing/Pictures/1615991837602.png")
        logo = pygame.image.load(image_path).convert_alpha()
        logo = pygame.transform.scale(logo, (160, 90))
    except Exception:
        pass

    transactions: List[Dict] = load_transactions()

    ProgramState = "MENU"
    history: List[str] = [
        "Welcome to Finance Tracker.",
        "1.Add Transaction",
        "2.View Total Balance",
        "3.View Recent Transactions",
        "4.Remove Transaction",
        "5.Edit Transaction (name & value)",
        "Q.Quit"
    ]
    
    current_entry: Dict[str, any] = {}
    Editing = -1
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

        if ProgramState == "MENU":
            question = "SELECT OPTION (1-5 or Q):"
        elif ProgramState == "GET_NAME":
            question = "ENTER ITEM NAME:"
        elif ProgramState == "GET_AMOUNT":
            name = current_entry.get('name', 'ITEM')
            question = f"ENTER AMOUNT FOR '{name}' (use - for expense):"
        elif ProgramState == "CONFIRM":
            name = current_entry.get('name', '')
            amt = current_entry.get('amount', 0.0)
            question = f"SAVE '{name}' (${amt:.2f})? (y/n):"
        elif ProgramState == "REMOVE_SELECT":
            question = "ENTER NUMBER TO REMOVE (0 to cancel):"
        elif ProgramState == "EDIT_SELECT":
            question = "ENTER NUMBER TO EDIT (0 to cancel):"
        elif ProgramState == "EDIT_NAME":
            question = "NEW NAME (leave blank to keep current):"
        elif ProgramState == "EDIT_AMOUNT":
            question = "NEW AMOUNT (leave blank to keep current):"
        else:
            question = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                    try:
                        clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
                        if clipboard:
                            pasted = clipboard.decode('utf-8', errors='ignore')
                            user_text += clean_text(pasted)[:CHARACTER_LIMIT - len(user_text)]
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

                    if not cmd and ProgramState == "MENU":
                        continue

                    history.append(f"{question} {user_text}")

                    if ProgramState == "MENU":
                        command_lower = cmd.lower()
                        if command_lower == "1":
                            ProgramState = "GET_NAME"
                            current_entry = {}
                        elif command_lower == "2":
                            total = sum(t.get('amount', 0) for t in transactions)
                            history.append(f"TOTAL BALANCE: ${total:.2f}")
                            history.append("─" * 60)
                        elif command_lower == "3":
                            if transactions:
                                history.append("RECENT TRANSACTIONS:")
                                for t in transactions[-10:]:
                                    history.append(f"  • {t.get('name', 'Unknown'):<30} ${t.get('amount', 0):>12.2f}")
                            else:
                                history.append("No transactions yet.")
                            history.append("─" * 60)
                        elif command_lower == "4":
                            ProgramState = "REMOVE_SELECT"
                            history.append("─" * 60)
                            history.append("RECENT TRANSACTIONS (most recent first):")
                            for i, t in enumerate(reversed(transactions[-15:]), 1):
                                history.append(f"  {i:2d}. {t.get('name', 'Unknown'):<28} ${t.get('amount', 0):>10.2f}")
                            history.append("─" * 60)
                        elif command_lower == "5":
                            ProgramState = "EDIT_SELECT"
                            history.append("─" * 60)
                            history.append("RECENT TRANSACTIONS (most recent first):")
                            for i, t in enumerate(reversed(transactions[-15:]), 1):
                                history.append(f"  {i:2d}. {t.get('name', 'Unknown'):<28} ${t.get('amount', 0):>10.2f}")
                            history.append("─" * 60)
                        elif command_lower in ["q", "quit", "exit"]:
                            running = False
                            continue
                        else:
                            history.append("Invalid option.")

                    elif ProgramState == "GET_NAME":
                        if cmd:
                            current_entry['name'] = cmd
                            ProgramState = "GET_AMOUNT"
                        else:
                            history.append("Error: Name cannot be empty.")

                    elif ProgramState == "GET_AMOUNT":
                        try:
                            amount = float(cmd.replace(',', '').strip())
                            current_entry['amount'] = amount
                            ProgramState = "CONFIRM"
                        except ValueError:
                            history.append("Error: Invalid number.")

                    elif ProgramState == "CONFIRM":
                        if cmd.lower() == "y":
                            transactions.append(current_entry.copy())
                            save_transactions(transactions)
                            history.append("✓ TRANSACTION SAVED SUCCESSFULLY.")
                        else:
                            history.append("Transaction cancelled.")
                        ProgramState = "MENU"
                        current_entry = {}

                    elif ProgramState == "REMOVE_SELECT":
                        try:
                            num = int(cmd)
                            if num == 0:
                                history.append("Removal cancelled.")
                            elif 1 <= num <= min(15, len(transactions)):
                                actual_idx = len(transactions) - num
                                removed = transactions.pop(actual_idx)
                                save_transactions(transactions)
                                history.append(f"✓ REMOVED: {removed.get('name', '')} (${removed.get('amount', 0):.2f})")
                            else:
                                history.append("Invalid number.")
                        except ValueError:
                            history.append("Please enter a valid number.")
                        ProgramState = "MENU"

                    elif ProgramState == "EDIT_SELECT":
                        try:
                            num = int(cmd)
                            if num == 0:
                                history.append("Edit cancelled.")
                                ProgramState = "MENU"
                            elif 1 <= num <= min(15, len(transactions)):
                                Editing = len(transactions) - num
                                ProgramState = "EDIT_NAME"
                                current = transactions[Editing]
                                history.append(f"Editing: {current.get('name')} (${current.get('amount'):.2f})")
                            else:
                                history.append("Invalid number.")
                                ProgramState = "MENU"
                        except ValueError:
                            history.append("Please enter a valid number.")
                            ProgramState = "MENU"

                    elif ProgramState == "EDIT_NAME":
                        if cmd:
                            transactions[Editing]['name'] = cmd
                            history.append(f"Name updated to: {cmd}")
                        else:
                            history.append("Name unchanged.")
                        ProgramState = "EDIT_AMOUNT"

                    elif ProgramState == "EDIT_AMOUNT":
                        if cmd:
                            try:
                                new_amt = float(cmd.replace(',', '').strip())
                                transactions[Editing]['amount'] = new_amt
                                history.append(f"Amount updated to: ${new_amt:.2f}")
                            except ValueError:
                                history.append("Invalid amount - amount unchanged.")
                        else:
                            history.append("Amount unchanged.")
                        save_transactions(transactions)
                        history.append("TRANSACTION EDITED SUCCESSFULLY.")
                        ProgramState = "MENU"
                        Editing = -1

                    if len(history) > MAX_HISTORY:
                        history = history[-MAX_HISTORY:]

                    user_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    if ProgramState != "MENU":
                        ProgramState = "MENU"
                        current_entry = {}
                        Editing = -1
                        history.append("← Action cancelled.")
                    else:
                        running = False
                else:
                    if event.unicode.isprintable() and len(user_text) < CHARACTER_LIMIT:
                        user_text += event.unicode

        screen.fill(BG_COLOR)

        if logo:
            logo_x = WIDTH - logo.get_width() - 20
            logo_y = 15
            screen.blit(logo, (logo_x, logo_y))

        y_pos = HISTORY_START_Y
        start_idx = max(0, len(history) - VISIBLE_LINES)

        for i in range(VISIBLE_LINES):
            if start_idx + i >= len(history):
                break
            line = history[start_idx + i]

            if "Error" in line or "Invalid" in line:
                color = ERROR_COLOR
            elif "SAVED" in line or "TOTAL" in line or "✓" in line or "BALANCE" in line or "REMOVED" in line or "EDITED" in line:
                color = SUCCESS_COLOR
            else:
                color = HISTORY_COLOR

            try:
                surf = font.render(line, True, color)
                screen.blit(surf, (30, y_pos))
            except Exception:
                safe_line = clean_text(line)
                surf = font.render(safe_line[:200], True, color)
                screen.blit(surf, (30, y_pos))

            y_pos += LINE_HEIGHT

        prompt_surf = font.render(question, True, PROMPT_COLOR)
        screen.blit(prompt_surf, (30, y_pos))
        y_pos += LINE_HEIGHT

        cursor = "_" if show_cursor and ProgramState != "MENU" else " "
        cursor_text = f"> {user_text}{cursor}"
        input_surf = font.render(cursor_text, True, TEXT_COLOR)
        screen.blit(input_surf, (30, y_pos))

        status = f"Transactions: {len(transactions)} | State: {ProgramState} | History lines: {len(history)}"
        status_surf = small_font.render(status, True, (100, 100, 100))
        screen.blit(status_surf, (30, HEIGHT - 55))

        help_text = "Ctrl+V Paste | Ctrl+C Copy | ESC to cancel"
        help_surf = small_font.render(help_text, True, (80, 80, 80))
        screen.blit(help_surf, (30, HEIGHT - 32))

        if len(history) > VISIBLE_LINES:
            track_height = HEIGHT - 120
            thumb_height = max(20, int(track_height * (VISIBLE_LINES / len(history))))
            thumb_y = HEIGHT - 120 - thumb_height

            pygame.draw.rect(screen, (60, 60, 60), (WIDTH - 14, 20, 8, track_height))
            pygame.draw.rect(screen, (180, 180, 200), (WIDTH - 14, thumb_y, 8, thumb_height))

        pygame.display.flip()
        clock.tick(60)

    save_transactions(transactions)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()