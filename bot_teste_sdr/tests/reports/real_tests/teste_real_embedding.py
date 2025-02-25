# tests/reports/real_data_tests/test_real_embedding.py
import unittest
import os
from src.reports.embedding_extractor import EmbeddingExtractor
from src.reports.daily_report import DailyReport
from src.reports.fetcher_base import ConversationsFetcher
from src.reports.chat_parser import load_labeled_history

class LocalFileFetcher(ConversationsFetcher):
    def fetch_today_conversations(self):
        # Converte conversas rotuladas do chatbase em dicionário
        all_conv = load_labeled_history(base_dir="assets/chatbase")
        final_list = []
        for conv in all_conv:
            final_list.append({
                "lead_id": conv["label"],
                "mensagens": conv["mensagens"],
                "timestamp": conv["mensagens"][0]["timestamp"] if conv["mensagens"] else "N/A"
            })
        return final_list

class TestRealEmbedding(unittest.TestCase):
    def test_train_and_report(self):
        # 1) Treina
        ext = EmbeddingExtractor()
        X, y = ext.build_dataset(base_dir="assets/chatbase")
        self.assertGreater(len(X), 0, "Esperava ter msgs para treinar.")
        ext.train_classifier(X, y)
        ext.save_classifier("test_model_store.json")

        # 2) Roda daily report
        fetcher = LocalFileFetcher()
        dr = DailyReport(fetcher=fetcher, model_json="test_model_store.json")
        result = dr.generate_report()
        print("Relatório real c/ embeddings:", result)

        # Cleanup
        if os.path.exists("test_model_store.json"):
            os.remove("test_model_store.json")

if __name__ == "__main__":
    unittest.main()
