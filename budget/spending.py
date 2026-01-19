from budget.storage import ensure_month

def add_daily_expense(data, month, day, amount, note="", category="Other"):
    ensure_month(data, month)

    data["monthly"][month]["expenses"].append({
        "day": day,
        "amount": amount,
        "note": note,
        "category": category
    })

    return data

def set_fixed_expense(data, name, amount, category="Other"):
    data = json.load(file)
    if "fixed_expenses" not in data:
        data["fixed_expenses"] = []

    data["fixed_expenses"].append({
        "name": name,
        "amount": amount,
        "category": category
    })

    return data

def total_fixed_expenses(data):
    return sum(
        exp["amount"]
        for exp in data.get("fixed_expenses", [])
    )


def total_monthly_expenses(data, month):
    fixed_total = 0

    for exp in data.get("fixed_expenses", {}).values():
        if isinstance(exp, dict):
            fixed_total += exp.get("amount", 0)
        else:
            fixed_total += exp

    daily_total = sum(
        expense["amount"]
        for expense in data["monthly"].get(month, {}).get("expenses", [])
    )

    return fixed_total + daily_total

