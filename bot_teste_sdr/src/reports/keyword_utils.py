# src/reports/keyword_utils.py
import json
import os

def load_keywords_db(keywords_file="keywords_db.json"):
    if os.path.exists(keywords_file):
        with open(keywords_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_keywords_db(db, keywords_file="keywords_db.json"):
    with open(keywords_file, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)
