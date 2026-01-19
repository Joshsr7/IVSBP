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

    if not isinstance(data, dict):
        data = {}

    if "fixed_expenses" not in data or not isinstance(data["fixed_expenses"], list):
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

    fixed_total = sum(
        exp.get("amount", 0)
        for exp in data.get("fixed_expenses", [])
    )

    daily_total = sum(
        expense.get("amount", 0)
        for expense in data.get("monthly", {})
                          .get(month, {})
                          .get("expenses", [])
    )

    return fixed_total + daily_total


