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

CHARACTER_LIMIT = 300_000_000
MAX_HISTORY = 20_000

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
                    if not cmd and state == "MENU":
                        continue

                    history.append(f"{active_question} {user_text}")

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
                            history.append("─" * 60)
                            processed = True
                        elif cmd_lower == "3":
                            if transactions:
                                history.append("RECENT TRANSACTIONS:")
                                for t in transactions[-10:]:
                                    history.append(f"  • {t.get('name', 'Unknown'):<30} ${t.get('amount', 0):>12.2f}")
                            else:
                                history.append("No transactions yet.")
                            history.append("─" * 60)
                            processed = True
                        elif cmd_lower in ["q", "quit", "exit"]:
                            running = False
                            continue
                        else:
                            history.append("Invalid option.")

                    elif state == "GET_NAME":
                        if cmd:
                            current_entry['name'] = cmd
                            state = "GET_AMOUNT"
                            processed = True
                        else:
                            history.append("Error: Name cannot be empty.")

                    elif state == "GET_AMOUNT":
                        try:
                            amount = float(cmd.replace(',', '').strip())
                            current_entry['amount'] = amount
                            state = "CONFIRM"
                            processed = True
                        except ValueError:
                            history.append("Error: Invalid number.")

                    elif state == "CONFIRM":
                        if cmd.lower() == "y":
                            transactions.append(current_entry.copy())
                            saved_ok = save_transactions(transactions)   # ← Save immediately
                            if saved_ok:
                                history.append("✓ TRANSACTION SAVED SUCCESSFULLY.")
                            else:
                                history.append("✓ TRANSACTION SAVED (in memory) - File write failed.")
                        else:
                            history.append("Transaction cancelled.")
                        state = "MENU"
                        current_entry = {}
                        processed = True

                    if len(history) > MAX_HISTORY:
                        history = history[-MAX_HISTORY:]

                    user_text = ""

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

        # Rendering
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
            elif "SAVED" in line or "TOTAL" in line or "✓" in line or "BALANCE" in line:
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

        prompt_surf = font.render(active_question, True, PROMPT_COLOR)
        screen.blit(prompt_surf, (30, y_pos))
        y_pos += LINE_HEIGHT

        cursor = "_" if show_cursor and state != "MENU" else " "
        cursor_text = f"> {user_text}{cursor}"
        input_surf = font.render(cursor_text, True, TEXT_COLOR)
        screen.blit(input_surf, (30, y_pos))

        status = f"Transactions: {len(transactions)} | State: {state} | History lines: {len(history)}"
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

    # Final save on exit (safety)
    save_transactions(transactions)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()