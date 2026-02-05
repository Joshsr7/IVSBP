import json
import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATA_FOLDER = os.path.join(BASE_DIR, "data", "users")

def get_user_file(username):

    return os.path.join(DATA_FOLDER, f"{username}.json")

def load_user_data(username):

    file_path = get_user_file(username)

    default_data = {
        "fixed_income": 0,
        "fixed_expenses": [],
        "monthly": {}
    }

    if not os.path.exists(file_path):
        save_user_data(username, default_data)
        return default_data

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        save_user_data(username, default_data)
        return default_data

    
    if "fixed_expenses" not in data or not isinstance(data["fixed_expenses"], list):
        data["fixed_expenses"] = []

    if "monthly" not in data or not isinstance(data["monthly"], dict):
        data["monthly"] = {}

    
    return data


def save_user_data(username, data):

    os.makedirs(DATA_FOLDER, exist_ok=True)

    with open(get_user_file(username), "w") as file:
        json.dump(data, file, indent=4)

def ensure_month(data, month):

    if "monthly" not in data:
        data["monthly"] = {}

    if month not in data["monthly"]:
        data["monthly"][month] = {}

    if "income" not in data["monthly"][month]:
        data["monthly"][month]["income"] = []

    if "expenses" not in data["monthly"][month]:
        data["monthly"][month]["expenses"] = []




def delete_income(username, data, month, index):
    try:
        data["monthly"][month]["income"].pop(index)
        save_user_data(username, data)
    except (KeyError, IndexError):
        pass


def delete_expense(username, data, month, index):
    try:
        data["monthly"][month]["expenses"].pop(index)
        save_user_data(username, data)
    except (KeyError, IndexError):
        pass
