# src/reports/keyword_extractor.py
import os
from .chat_parser import load_labeled_history
from .keyword_utils import load_keywords_db, save_keywords_db

class KeywordExtractor:
    """
    Processa o histórico rotulado (success/fail) para extrair
    palavras-chave relacionadas a cada label.
    """

    def __init__(self, keywords_file="keywords_db.json"):
        self.keywords_file = keywords_file
        # Carrega db existente ou inicia vazio
        self.keywords_db = load_keywords_db(self.keywords_file)

    def process_labeled_history(self, base_dir="chatbase"):
        """
        Lê conversas rotuladas e atualiza self.keywords_db
        com tokens encontrados.
        """
        conversas = load_labeled_history(base_dir=base_dir)
        for conv in conversas:
            label = conv["label"]  # 'agendou' ou 'nao_agendou'
            mensagens = conv["mensagens"]
            self.keywords_db.setdefault(label, [])

            # Exemplo simples: extrai tokens das últimas 2 mensagens do lead
            for msg in mensagens[-2:]:
                if msg["from"] == "lead":
                    tokens = msg["text"].lower().split()
                    for t in tokens:
                        if t not in self.keywords_db[label]:
                            self.keywords_db[label].append(t)

        save_keywords_db(self.keywords_db, self.keywords_file)
        return self.keywords_db
