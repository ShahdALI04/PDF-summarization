#chat_history.py
import json
import os

HISTORY_FILE = "storage/chat_history.json"

def load_history(session_id):
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(session_id, [])

def save_history(session_id, question, answer):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    if session_id not in data:
        data[session_id] = []
    data[session_id].append({"question": question, "answer": answer})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
