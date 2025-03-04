# src/reports/daily_report.py
import os
from datetime import datetime

from .fetcher_base import ConversationsFetcher
from .embedding_extractor import EmbeddingExtractor

class DailyReport:
    def __init__(self, fetcher, model_store="output/model_store.json"):
        """
        Inicializa o gerador de relatórios diários.
        - `fetcher`: Método para buscar conversas (ex: LocalFileFetcher).
        - `model_store`: Caminho do modelo treinado.
        """
        self.fetcher = fetcher
        self.extractor = EmbeddingExtractor(model_store=model_store)
        self.extractor.load_classifier()

    def generate_report(self):
        """ Gera o relatório baseado nas conversas da base `test/` """
        conversas = self.fetcher.fetch_today_conversations()
        if not conversas:
            print("⚠️ Nenhuma conversa encontrada para análise!")
            return {}

        report = {"total_conversas": len(conversas), "detalhes": []}

        for conv in conversas:
            label_pred = self.extractor.predict_label(" ".join([msg["text"] for msg in conv["mensagens"]]))
            report["detalhes"].append({"lead_id": conv["lead_id"], "predicao": label_pred})

        return report
