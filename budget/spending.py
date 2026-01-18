from budget.storage import ensure_month

def add_daily_expense(data, month, day, amount, note=""):
    ensure_month(data, month)

    data["monthly"][month]["expenses"].append({
        "day": day,
        "amount": amount,
        "note": note
    })

    return data

def set_fixed_expense(data, name, amount):
    if "fixed_expenses" not in data:
        data["fixed_expenses"] = {}
    data["fixed_expenses"][name] = amount
    return data

def total_fixed_expenses(data):

    return sum(data["fixed_expenses"].values())


def total_monthly_expenses(data, month):
    fixed_total = sum(data["fixed_expenses"].values())
    daily_total = sum(
        expense["amount"]
        for expense in data["monthly"].get(month, {}).get("expenses", [])
    )
    return fixed_total + daily_total
