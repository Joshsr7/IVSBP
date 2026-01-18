import json
import os
import hashlib


USERS_FILE = "data/users/users.json"


def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    os.makedirs("data/users", exist_ok=True)

    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)
    

def signup(username, password):
    users = load_users()

    if username in users: 
        return False, "Username already exists"

    users[username] = hash_password(password)
    save_users(users)

    return True, "Account created"

def login(username, password):
    users = load_users()

    if username not in users:
        return False, "User not found"

    if users[username] != hash_password(password):
        return False, "Incorrect password"

    return True, "Login successful"