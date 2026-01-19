import json
import os


DATA_FOLDER = "data/users"

def get_user_file(username):

    return os.path.join(DATA_FOLDER, f"{username}.json")

def load_user_data(username):

    file_path = get_user_file(username)

    default_data = {
        "fixed_income": 0,
        "fixed_expenses": {},
        "monthly": {}
    }

    if not os.path.exists(file_path):
        save_user_data(username, default_data)
        return default_data
    
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        save_user_data(username, default_data)
        return default_data


def save_user_data(username, data):

    os.makedirs(DATA_FOLDER, exist_ok=True)

    with open(get_user_file(username), "w") as file:
        json.dump(data, file, indent=4)

def ensure_month(data, month):

    if month not in data:
        data["monthly"] = {}
    if month not in data["monthly"]:
        data["monthly"][month] = {
            "income": [],
            "expenses": []
        }