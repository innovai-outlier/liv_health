# tests/reports/real_tests/teste_real_embedding.py

import unittest
import os
from src.reports.fetcher_base import ConversationsFetcher
from src.reports.chat_parser import load_labeled_history
from src.reports.embedding_extractor import EmbeddingExtractor
from src.reports.daily_report import DailyReport

class LocalFileFetcher(ConversationsFetcher):
    """
    Corrigido para retornar cada conversa no formato:
    {
      "label": conv["label"],
      "lead_id": conv["lead_id"],
      "mensagens": conv["mensagens"],
      "timestamp": ...
    }
    para manter consistência com o parser.
    """
    def fetch_today_conversations(self):
        # Converte conversas rotuladas do chatbase em dicionário
        all_conv = load_labeled_history(base_dir="assets/chatbase")
        final_list = []
        for conv in all_conv:
            # conv já tem: { 'label': 'agendou' ou 'nao_agendou'..., 'lead_id':..., 'mensagens': [...], ... }
            final_list.append({
                "label": conv["label"],
                "lead_id": conv["lead_id"],
                "mensagens": conv["mensagens"],
                "timestamp": conv["mensagens"][0]["timestamp"] if conv["mensagens"] else "N/A"
            })
        return final_list

class TestRealEmbedding(unittest.TestCase):
    def setUp(self):
        self.temp_model_store = "test_model_store.json"
        # Limpa se existir
        if os.path.exists(self.temp_model_store):
            os.remove(self.temp_model_store)

    def tearDown(self):
        if os.path.exists(self.temp_model_store):
            os.remove(self.temp_model_store)

    def test_train_and_report(self):
        # 1) Treinar o modelo
        extractor = EmbeddingExtractor()
        X, y = extractor.build_dataset(base_dir="assets/chatbase")
        self.assertGreater(len(X), 0, "Esperava ter mensagens para treinar, mas o dataset está vazio.")
        
        extractor.train_classifier(X, y)
        extractor.save_classifier(self.temp_model_store)

        # 2) Rodar daily report usando o fetcher local
        fetcher = LocalFileFetcher()
        dr = DailyReport(fetcher=fetcher, model_store=self.temp_model_store)
        result = dr.generate_report()

        print("Relatório real com embeddings:", result)
        self.assertIn("data", result)
        self.assertIn("detalhes", result)

if __name__ == "__main__":
    unittest.main()
