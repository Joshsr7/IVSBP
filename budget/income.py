from budget.storage import ensure_month, save_user_data

def set_fixed_income(username, data, amount):
    data["fixed_income"] = float(amount)
    save_user_data(username, data)
    return data

def add_extra_income(username, data, month, day, amount, note=""):
    ensure_month(data, month)

    data["monthly"][month]["income"].append({
        "day": day,
        "amount": float(amount),
        "note": note
    })

    
    save_user_data(username, data)

    return data

def total_monthly_income(data, month):
    fixed = data["fixed_income"]

    extras = sum(
        item["amount"]
        for item in data["monthly"].get(month, {}).get("income", [])
    )

    return fixed + extras