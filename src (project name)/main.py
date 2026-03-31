import pygame
import sys
import csv
import json
from pathlib import Path
from typing import List, Dict
import matplotlib.pyplot as plt
import io
from datetime import date
from collections import defaultdict

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
MAX_HISTORY = 25

CSV_FILE = Path("docs\Expenses.csv")
SETTINGS_FILE = Path("docs/settings.json")

def load_transactions() -> List[Dict]:
    transactions = []
    if CSV_FILE.exists():
        try:
            with open(CSV_FILE, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                today_str = date.today().isoformat()
                for row in reader:
                    try:
                        row = dict(row)
                        row['amount'] = float(row['amount'])
                        if 'type' not in row or row['type'] not in ('income', 'expense'):
                            row['type'] = 'expense'
                            row['detail'] = row.pop('name', 'Unknown') if 'name' in row else 'Unknown'
                        if 'date' not in row or not row['date']:
                            row['date'] = today_str
                        if 'detail' not in row or not row['detail']:
                            row['detail'] = 'Unknown'
                        transactions.append(row)
                    except (ValueError, KeyError):
                        pass
        except Exception as e:
            print(f"Warning: Could not load transactions: {e}")
    return transactions

def save_transactions(transactions: List[Dict]) -> bool:
    try:
        CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
            fieldnames = ['date', 'type', 'amount', 'detail']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for t in transactions:
                writer.writerow({
                    'date': t.get('date', ''),
                    'type': t.get('type', 'expense'),
                    'amount': t.get('amount', 0),
                    'detail': t.get('detail', '')
                })
        return True
    except Exception as e:
        print(f"Warning: Could not save transactions: {e}")
        return False

def load_settings() -> Dict:
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {'savings_goal': 0.0}

def save_settings(settings: Dict):
    try:
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except Exception:
        pass

def calculate_balance(transactions: List[Dict]):
    income = sum(t['amount'] for t in transactions if t.get('type') == 'income')
    expense = sum(t['amount'] for t in transactions if t.get('type') == 'expense')
    net = income - expense
    return income, expense, net

def create_expense_pie(transactions: List[Dict]):
    expense_by_cat = defaultdict(float)
    for t in transactions:
        if t.get('type') == 'expense':
            cat = t.get('detail', 'Uncategorized')
            expense_by_cat[cat] += t.get('amount', 0)

    if not expense_by_cat:
        return None

    labels = list(expense_by_cat.keys())
    values = list(expense_by_cat.values())
    colors = ["red", "gold", "lightskyblue", "lightcoral", "limegreen", "violet", "orange",
              "cyan", "magenta", "yellowgreen"] * 3

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(values, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close(fig)
    surface = pygame.image.load(buf, 'chart.png')
    return surface, surface.get_rect(center=(WIDTH // 2, 280))

def clean_text(text: str) -> str:
    if not text:
        return ""
    return ''.join(c for c in text if c >= ' ' or c in '\t\n').strip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Finance Tracker  Income, Expenses & Goal Tracker")

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
    settings = load_settings()
    savings_goal: float = settings.get('savings_goal', 0.0)

    ProgramState = "MENU"
    history: List[str] = [
        "Welcome to Finance Tracker (v2)",
        "1. Add Income",
        "2. Add Expense",
        "3. View Balance & Goal Progress",
        "4. View Recent Transactions",
        "5. Remove Transaction",
        "6. Edit Transaction",
        "7. View Expense Pie Chart (by Category)",
        "8. Set Savings Goal",
        "Q. Quit"
    ]

    current_entry: Dict[str, any] = {}
    Editing = -1
    user_text = ""
    running = True
    clock = pygame.time.Clock()

    pie_chart_surface = None
    pie_chart_rect = None

    last_blink = 0
    show_cursor = True

    while running:
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - last_blink > 0.5:
            show_cursor = not show_cursor
            last_blink = current_time

        if ProgramState == "MENU":
            question = "SELECT OPTION (1-8 or Q):"
        elif ProgramState == "GET_DATE":
            ttype = current_entry.get('type', 'income').upper()
            question = f"ENTER DATE FOR {ttype} (YYYY-MM-DD) or Enter for today:"
        elif ProgramState == "GET_AMOUNT":
            question = "ENTER AMOUNT:"
        elif ProgramState == "GET_DETAIL":
            detail_type = "SOURCE" if current_entry.get('type') == 'income' else "CATEGORY"
            question = f"ENTER {detail_type}:"
        elif ProgramState == "CONFIRM":
            ttype = current_entry.get('type', '').upper()
            dt = current_entry.get('date', '')
            det = current_entry.get('detail', '')
            amt = current_entry.get('amount', 0.0)
            question = f"SAVE {ttype} {dt} '{det}' ${amt:.2f}? (y/n):"
        elif ProgramState == "REMOVE_SELECT":
            question = "ENTER NUMBER TO REMOVE (0 to cancel):"
        elif ProgramState == "EDIT_SELECT":
            question = "ENTER NUMBER TO EDIT (0 to cancel):"
        elif ProgramState == "EDIT_DETAIL":
            ttype = transactions[Editing].get('type', 'expense').upper()
            question = f"NEW {ttype} DETAIL (blank to keep):"
        elif ProgramState == "EDIT_AMOUNT":
            question = "NEW AMOUNT (blank to keep):"
        elif ProgramState == "SET_GOAL":
            question = f"SET NEW SAVINGS GOAL (current: ${savings_goal:.2f}):"
        elif ProgramState == "VIEW_PIE":
            question = ""
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
                    Command = user_text.strip()
                    if not Command and ProgramState == "MENU":
                        continue

                    history.append(f"{question} {user_text}")

                    if ProgramState == "MENU":
                        Command_Prompt = Command.lower()
                        if Command_Prompt == "1":
                            ProgramState = "GET_DATE"
                            current_entry = {'type': 'income'}
                        elif Command_Prompt == "2":
                            ProgramState = "GET_DATE"
                            current_entry = {'type': 'expense'}
                        elif Command_Prompt == "3":
                            income, expense, net = calculate_balance(transactions)
                            progress = 0
                            if savings_goal > 0:
                                progress = max(0, min(100, (net / savings_goal) * 100))
                            history.append("BALANCE SUMMARY:")
                            history.append(f"  Income:      +${income:.2f}")
                            history.append(f"  Expenses:    -${expense:.2f}")
                            history.append(f"  Net Balance: ${net:.2f}")
                            if savings_goal > 0:
                                history.append(f"  Goal progress: {progress:.1f}% towards ${savings_goal:.2f}")
                            else:
                                history.append("  No savings goal set.")
                            history.append("─" * 60)
                        elif Command_Prompt == "4":
                            history.append("─" * 60)
                            history.append("RECENT TRANSACTIONS (newest first):")
                            for t in transactions[-15:]:
                                typ = t.get('type', 'E')[0].upper()
                                dt = t.get('date', '????')
                                det = t.get('detail', 'Unknown')[:25]
                                amt = t.get('amount', 0)
                                sign = "+" if t.get('type') == 'income' else "-"
                                history.append(f"  {dt} {typ} {det:<25} {sign}${amt:>8.2f}")
                            history.append("─" * 60)
                        elif Command_Prompt == "5":
                            ProgramState = "REMOVE_SELECT"
                            history.append("─" * 60)
                            history.append("RECENT TRANSACTIONS (newest first):")
                            for i, t in enumerate(reversed(transactions[-15:]), 1):
                                typ = t.get('type', 'E')[0].upper()
                                dt = t.get('date', '????')
                                det = t.get('detail', 'Unknown')[:25]
                                amt = t.get('amount', 0)
                                sign = "+" if t.get('type') == 'income' else "-"
                                history.append(f"  {i:2d}. {dt} {typ} {det:<25} {sign}${amt:>8.2f}")
                            history.append("─" * 60)
                        elif Command_Prompt == "6":
                            ProgramState = "EDIT_SELECT"
                            history.append("─" * 60)
                            history.append("RECENT TRANSACTIONS (newest first):")
                            for i, t in enumerate(reversed(transactions[-15:]), 1):
                                typ = t.get('type', 'E')[0].upper()
                                dt = t.get('date', '????')
                                det = t.get('detail', 'Unknown')[:25]
                                amt = t.get('amount', 0)
                                sign = "+" if t.get('type') == 'income' else "-"
                                history.append(f"  {i:2d}. {dt} {typ} {det:<25} {sign}${amt:>8.2f}")
                            history.append("─" * 60)
                        elif Command_Prompt == "7":
                            pie_data = create_expense_pie(transactions)
                            if pie_data is None:
                                history.append("No expenses recorded yet for pie chart.")
                                history.append("─" * 60)
                            else:
                                pie_chart_surface, pie_chart_rect = pie_data
                                ProgramState = "VIEW_PIE"
                                history.append("✓ Dynamic Expense Pie Chart displayed (by category).")
                                history.append("Press ESC to return.")
                                user_text = ""
                                continue
                        elif Command_Prompt == "8":
                            ProgramState = "SET_GOAL"
                        elif Command_Prompt in ["q", "quit", "exit"]:
                            running = False
                            continue
                        else:
                            history.append("Invalid option.")

                    elif ProgramState == "GET_DATE":
                        if not Command:
                            current_entry['date'] = date.today().isoformat()
                        else:
                            current_entry['date'] = Command.strip()
                        ProgramState = "GET_AMOUNT"

                    elif ProgramState == "GET_AMOUNT":
                        try:
                            current_entry['amount'] = float(Command.replace(',', '').strip())
                            ProgramState = "GET_DETAIL"
                        except ValueError:
                            history.append("Error: Invalid number.")

                    elif ProgramState == "GET_DETAIL":
                        if Command:
                            current_entry['detail'] = Command.strip()
                        else:
                            current_entry['detail'] = "Uncategorized" if current_entry.get('type') == 'expense' else "Unknown Source"
                        ProgramState = "CONFIRM"

                    elif ProgramState == "CONFIRM":
                        if Command.lower() == "y":
                            transactions.append(current_entry.copy())
                            save_transactions(transactions)
                            history.append("✓ TRANSACTION SAVED SUCCESSFULLY.")
                        else:
                            history.append("Transaction cancelled.")
                        ProgramState = "MENU"
                        current_entry = {}

                    elif ProgramState == "REMOVE_SELECT":
                        try:
                            num = int(Command)
                            if num == 0:
                                history.append("Removal cancelled.")
                            elif 1 <= num <= min(15, len(transactions)):
                                actual_idx = len(transactions) - num
                                removed = transactions.pop(actual_idx)
                                save_transactions(transactions)
                                history.append(f"✓ REMOVED: {removed.get('date')} {removed.get('detail')} (${removed.get('amount'):.2f})")
                            else:
                                history.append("Invalid number.")
                        except ValueError:
                            history.append("Please enter a valid number.")
                        ProgramState = "MENU"

                    elif ProgramState == "EDIT_SELECT":
                        try:
                            num = int(Command)
                            if num == 0:
                                history.append("Edit cancelled.")
                                ProgramState = "MENU"
                            elif 1 <= num <= min(15, len(transactions)):
                                Editing = len(transactions) - num
                                current = transactions[Editing]
                                history.append(f"Editing: {current.get('date')} {current.get('detail')} (${current.get('amount'):.2f})")
                                ProgramState = "EDIT_DETAIL"
                            else:
                                history.append("Invalid number.")
                                ProgramState = "MENU"
                        except ValueError:
                            history.append("Please enter a valid number.")
                            ProgramState = "MENU"

                    elif ProgramState == "EDIT_DETAIL":
                        if Command:
                            transactions[Editing]['detail'] = Command
                            history.append(f"Detail updated to: {Command}")
                        else:
                            history.append("Detail unchanged.")
                        ProgramState = "EDIT_AMOUNT"

                    elif ProgramState == "EDIT_AMOUNT":
                        if Command:
                            try:
                                new_amt = float(Command.replace(',', '').strip())
                                transactions[Editing]['amount'] = new_amt
                                history.append(f"Amount updated to: ${new_amt:.2f}")
                            except ValueError:
                                history.append("Invalid amount – unchanged.")
                        else:
                            history.append("Amount unchanged.")
                        save_transactions(transactions)
                        history.append("TRANSACTION EDITED SUCCESSFULLY.")
                        ProgramState = "MENU"
                        Editing = -1

                    elif ProgramState == "SET_GOAL":
                        try:
                            new_goal = float(Command.replace(',', '').strip())
                            if new_goal < 0:
                                new_goal = 0
                            savings_goal = new_goal
                            save_settings({'savings_goal': savings_goal})
                            history.append(f"✓ SAVINGS GOAL UPDATED TO ${savings_goal:.2f}")
                        except ValueError:
                            history.append("Invalid amount – goal unchanged.")
                        ProgramState = "MENU"

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
                        pie_chart_surface = None
                        history.append("← Action cancelled.")
                    else:
                        running = False
                else:
                    if event.unicode.isprintable() and len(user_text) < CHARACTER_LIMIT:
                        user_text += event.unicode

        screen.fill(BG_COLOR)

        if logo:
            screen.blit(logo, (WIDTH - logo.get_width() - 20, 15))

        if ProgramState == "VIEW_PIE" and pie_chart_surface is not None:
            screen.blit(pie_chart_surface, pie_chart_rect)
            title_surf = font.render("EXPENSES BY CATEGORY", True, PROMPT_COLOR)
            screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 40))
            instr_surf = small_font.render("Press ESC to return to menu", True, (200, 200, 200))
            screen.blit(instr_surf, (WIDTH // 2 - instr_surf.get_width() // 2, HEIGHT - 80))

        else:
            y_pos = HISTORY_START_Y
            start_idx = max(0, len(history) - VISIBLE_LINES)
            for i in range(VISIBLE_LINES):
                if start_idx + i >= len(history):
                    break
                line = history[start_idx + i]
                color = ERROR_COLOR if "Error" in line or "Invalid" in line else \
                        SUCCESS_COLOR if "✓" in line or "SAVED" in line or "BALANCE" in line or "UPDATED" in line else \
                        HISTORY_COLOR
                try:
                    surf = font.render(line, True, color)
                    screen.blit(surf, (30, y_pos))
                except Exception:
                    surf = font.render(clean_text(line)[:200], True, color)
                    screen.blit(surf, (30, y_pos))
                y_pos += LINE_HEIGHT

            prompt_surf = font.render(question, True, PROMPT_COLOR)
            screen.blit(prompt_surf, (30, y_pos))
            y_pos += LINE_HEIGHT

            cursor = "_" if show_cursor else " "
            input_surf = font.render(f"> {user_text}{cursor}", True, TEXT_COLOR)
            screen.blit(input_surf, (30, y_pos))

            if len(history) > VISIBLE_LINES:
                track_h = HEIGHT - 120
                thumb_h = max(20, int(track_h * (VISIBLE_LINES / len(history))))
                thumb_y = HEIGHT - 120 - thumb_h + 20
                pygame.draw.rect(screen, (60, 60, 60), (WIDTH - 14, 20, 8, track_h))
                pygame.draw.rect(screen, (180, 180, 200), (WIDTH - 14, thumb_y, 8, thumb_h))

        income_t, expense_t, net_t = calculate_balance(transactions)
        status = f"Transactions: {len(transactions)} | Net: ${net_t:.2f} | Goal: ${savings_goal:.2f} | State: {ProgramState}"
        status_surf = small_font.render(status, True, (100, 100, 100))
        screen.blit(status_surf, (30, HEIGHT - 55))

        help_surf = small_font.render("Ctrl+V Paste | Ctrl+C Copy | ESC cancel/return", True, (80, 80, 80))
        screen.blit(help_surf, (30, HEIGHT - 32))

        pygame.display.flip()
        clock.tick(60)

    save_transactions(transactions)
    save_settings({'savings_goal': savings_goal})
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()