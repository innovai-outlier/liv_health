# src/reports/synonyms_utils.py
import json
import os
from fuzzywuzzy import fuzz

def load_synonyms_db(path="synonyms_db.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_synonyms_db(db, path="synonyms_db.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

def find_synonym(match_word, synonyms, threshold=80):
    """
    Aplica fuzzy matching para localizar sinônimo em synonyms.
    synonyms = {
      'nota fiscal': ['nota', 'nf', 'recibo'],
      'receita': ['prescricao', 'remedio', ...],
      ...
    }
    Retorna a chave do sinônimo se achar, senão None
    """
    match_word_low = match_word.lower()
    for key, variants in synonyms.items():
        for variant in variants:
            ratio = fuzz.ratio(match_word_low, variant.lower())
            if ratio >= threshold:
                return key
    return None
