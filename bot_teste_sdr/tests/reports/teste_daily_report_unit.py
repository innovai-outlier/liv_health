# tests/reports/test_daily_report_unit.py

import unittest
import os
from src.reports.daily_report import DailyReport
from src.reports.fetcher_base import ConversationsFetcher

class MockFetcher(ConversationsFetcher):
    """
    Simula a coleta de conversas no formato que o parser real fornece:
      {
        "label": "agendou" ou "nao_agendou" etc.,
        "lead_id": "111",
        "mensagens": [
          {"from": "lead"/"assistente", "text": "...", "timestamp": "..."},
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
                    {"from": "assistente", "text": "Excelente", "timestamp": "2025-05-01 10:01"}
                ]
            },
            {
                "label": "nao_agendou",
                "lead_id": "222",
                "mensagens": [
                    {"from": "lead", "text": "só estou pesquisando", "timestamp": "2025-05-01 11:00"},
                    {"from": "assistente", "text": "Certo, fico à disposição!", "timestamp": "2025-05-01 11:01"}
                ]
            }
        ]

class TestDailyReportUnit(unittest.TestCase):
    def setUp(self):
        # Se o DailyReport precisar de um model_store ou algo assim, você pode simular
        self.mock_model_store = "mock_model_store.json"
        # Dependendo do seu fluxo, crie ou copie um model_store de teste aqui
        if os.path.exists(self.mock_model_store):
            os.remove(self.mock_model_store)
        # Opcionalmente, crie um model_store fictício ou deixe sem

    def tearDown(self):
        if os.path.exists(self.mock_model_store):
            os.remove(self.mock_model_store)

    def test_generate_report(self):
        # Instancia o fetcher
        fetcher = MockFetcher()
        # Se seu DailyReport espera um param model_store:
        dr = DailyReport(fetcher=fetcher, model_store=self.mock_model_store)
        resultado = dr.generate_report()

        print("Resultado do relatório (unit test):", resultado)

        # Exemplos de checks básicos
        self.assertIn("total_conversas", resultado)
        self.assertEqual(resultado["total_conversas"], 2)
        self.assertIn("detalhes", resultado)
        self.assertIsInstance(resultado["detalhes"], list)

if __name__ == "__main__":
    unittest.main()
