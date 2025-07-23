import json
import os

PATH = os.path.join(os.path.dirname(__file__), "users.json")

def load_users():
    if not os.path.exists(PATH):
        return []
    with open(PATH, "r") as f:
        return json.load(f)

def save_users(data):
    with open(PATH, "w") as f:
        json.dump(data, f, indent=2)
