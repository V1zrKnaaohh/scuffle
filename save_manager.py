import json

def save_data(data):
    with open("settings.json", "w") as f:
        json.dump(data, f)

def load_data():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"volume": 5, "state": "main_lobby"}