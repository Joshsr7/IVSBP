from budget.storage import ensure_month

def set_fixed_income(data, amount):
    data["fixed_income"] = amount
    return data

def add_extra_income(data, month, day, amount, note=""):
    ensure_month(data, month)

    data["monthly"][month]["income"].append({
        "day": day,
        "amount": amount,
        "note": note
    })

    return data

def total_monthly_income(data, month):
    fixed = data["fixed_income"]

    extras = sum(
        item["amount"]
        for item in data["monthly"].get(month, {}).get("income", [])
    )

    return fixed + extras