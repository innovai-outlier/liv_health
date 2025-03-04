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
        """ Testa a geração de embeddings e a criação do relatório usando `test/` """
        extractor = EmbeddingExtractor()
        X, y = extractor.build_dataset(base_type="test")
        
        assert len(X) > 0, "ERRO: Nenhuma amostra encontrada na base `test/`!"

        extractor.train_classifier(X, y)
        extractor.save_classifier()

        fetcher = LocalFileFetcher(base_type="test")
        report_generator = DailyReport(fetcher=fetcher, model_store=extractor.model_store)
        report = report_generator.generate_report()

        assert "total_conversas" in report, "ERRO: O relatório não contém conversas!"

if __name__ == "__main__":
    unittest.main()
