# src/reports/synonyms_extractor.py
import os
import re
from .chat_parser import load_labeled_history
from .synonyms_utils import load_synonyms_db, save_synonyms_db, find_synonym
from fuzzywuzzy import fuzz

class SynonymsExtractor:
    """
    Autoenriquece synonyms_db com novos termos que não batem em nenhum key
    Pergunta ao usuário ou (neste exemplo) coloca em 'pendentes' 
    """
    def __init__(self, path="synonyms_db.json"):
        self.path = path
        self.db = load_synonyms_db(path)
        if "pendentes" not in self.db:
            self.db["pendentes"] = []  # Tokens desconhecidos

    def process_labeled_history(self, base_dir="assets/chatbase"):
        conversas = load_labeled_history(base_dir=base_dir)
        for conv in conversas:
            for msg in conv["mensagens"]:
                # tokens
                tokens = re.findall(r"\w+", msg["text"].lower())
                for t in tokens:
                    # check se esse token encaixa num syn
                    existing_key = find_synonym(t, self.db, threshold=85)
                    if not existing_key:
                        # Se não achar => add em pendentes
                        if t not in self.db["pendentes"]:
                            self.db["pendentes"].append(t)
        save_synonyms_db(self.db, self.path)
        return self.db

    def integrate_pendentes(self, key):
        """
        Exemplo: move itens de pendentes para um key, perguntando ao usuário
        se cada token deve entrar em synonyms_db[key].
        Ao final, salva no synonyms_db.json.
        """
        if key not in self.db:
            self.db[key] = []

        new_pendentes = []
        moved_tokens = 0

        # Percorre cada token pendente
        for token in self.db["pendentes"]:
            print(f"Token '{token}' encontrado em pendentes. Integrar ao sinônimo '{key}'? [y/n]")
            res = input().strip().lower()
            if res == 'y':
                # Adiciona token a db[key]
                if token not in self.db[key]:
                    self.db[key].append(token)
                moved_tokens += 1
            else:
                # Mantém o token em pendentes
                new_pendentes.append(token)

        self.db["pendentes"] = new_pendentes
        save_synonyms_db(self.db, self.path)

        print(f"Integrados {moved_tokens} tokens ao sinônimo '{key}'. Pendentes restantes: {len(new_pendentes)}.")
