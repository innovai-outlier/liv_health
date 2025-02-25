# tests/reports/real_tests/test_real_daily_report.py

import unittest
import os
from src.reports.fetcher_base import ConversationsFetcher
from src.reports.daily_report import DailyReport

class MockDailyReportFetcher(ConversationsFetcher):
    """
    Retorna conversas no formato esperado:
    {
      "label": "agendou" ou "nao_agendou" ou etc.,
      "lead_id": "some_lead_id",
      "mensagens": [
        { "from": "lead"/"assistente", "text": "...", "timestamp": "..." },
        ...
      ]
    }
    """
    def fetch_today_conversations(self):
        return [
            {
                "label": "agendou",
                "lead_id": "111",
                "mensagens": [
                    {"from": "lead", "text": "vou agendar agora", "timestamp": "2025-05-01 10:00"},
                    {"from": "assistente", "text": "Excelente!", "timestamp": "2025-05-01 10:01"}
                ]
            },
            {
                "label": "nao_agendou",
                "lead_id": "222",
                "mensagens": [
                    {"from": "lead", "text": "só estou pesquisando", "timestamp": "2025-05-01 11:00"},
                    {"from": "assistente", "text": "Sem problemas!", "timestamp": "2025-05-01 11:01"}
                ]
            }
        ]

class TestRealDailyReport(unittest.TestCase):
    def setUp(self):
        # Se for usar embeddings, definimos model_store ou outro param
        self.temp_model_store = "temp_model_store.json"
        if os.path.exists(self.temp_model_store):
            os.remove(self.temp_model_store)

    def tearDown(self):
        if os.path.exists(self.temp_model_store):
            os.remove(self.temp_model_store)

    def test_daily_report_real_data(self):
        # Instancia o fetcher usando o template correto
        fetcher = MockDailyReportFetcher()
        # Se o DailyReport espera um param model_store:
        dr = DailyReport(fetcher=fetcher, model_store=self.temp_model_store)
        # Gera o relatório
        result = dr.generate_report()

        print("Resultado do relatório (real test) =>", result)
        self.assertIn("data", result)
        self.assertIn("detalhes", result)
        self.assertEqual(result["total_conversas"], 2)

if __name__ == "__main__":
    unittest.main()
