import helper


def load_settings():
    goal = helper.load_goal()
    budgets = helper.load_budgets()
    return {"goal": goal, "budgets": budgets}


def save_settings(settings):
    goal = settings.get("goal", 0)
    budgets = settings.get("budgets", {})
    helper.save_goal(goal)
    helper.save_budgets(budgets)


def set_goal(settings, amount):
    settings["goal"] = amount

def get_goal(settings):
    return settings.get("goal", 0)

def goal_progress(current_balance, goal):
    if goal <= 0:
        return 0
    return (current_balance / goal) * 100


def set_budget(settings, category, amount):
    if "budgets" not in settings:
        settings["budgets"] = {}
    settings["budgets"][category] = amount

def get_budget(settings, category):
    return settings.get("budgets", {}).get(category, 0)

def all_budgets(settings):
    return settings.get("budgets", {})


def check_budget(expenses, settings):
    warnings = []
    budgets = settings.get("budgets", {})

    totals = {}
    for e in expenses:
        cat = e.get("category")
        if not cat:
            continue
        totals[cat] = totals.get(cat, 0) + e["amount"]

    for cat, spent in totals.items():
        limit = budgets.get(cat)
        if limit is not None and spent > limit:
            warnings.append(f"{cat} over budget! (${spent:.2f} / ${limit:.2f})")

    return warnings