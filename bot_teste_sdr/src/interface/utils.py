import json
import os

def carregar_json(file_path):
    """ Carrega um arquivo JSON, verificando se existe """
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
