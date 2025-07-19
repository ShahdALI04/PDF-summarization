import json
import os

HISTORY_FILE = "chat_history.json"

def load_history(username):
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(username, [])

def save_history(username, question, answer):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    if username not in data:
        data[username] = []

    data[username].append({"question": question, "answer": answer})

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
