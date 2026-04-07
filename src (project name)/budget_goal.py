import json
from pathlib import Path

SETTINGS_FILE = Path(r"docs\settings.json")

def load_settings():
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"goal": 0, "budgets": {}}

def save_settings(settings):
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

# ---- Savings Goal ----
def set_goal(settings, amount):
    settings["goal"] = max(0, amount)

def goal_progress(balance, goal):
    if goal <= 0:
        return 0
    return min(100, (balance / goal) * 100)

# ---- Budget ----
def set_budget(settings, category, amount):
    settings["budgets"][category] = amount

def compare_budget(spending, budgets):
    report = []
    for cat, limit in budgets.items():
        used = spending.get(cat, 0)
        status = "OK" if used <= limit else "OVER"
        report.append((cat, used, limit, status))
    return report