# tests/reports/test_daily_report_unit.py
import unittest
from src.reports.daily_report import DailyReport
from src.reports.fetcher_base import ConversationsFetcher

class MockFetcher(ConversationsFetcher):
    def fetch_today_conversations(self):
        return [
            {
                "lead_id": "111",
                "mensagens": [
                    {"from": "lead", "text": "vou agendar agora", "timestamp": "2025-05-01 10:00"},
                    {"from": "assistente", "text": "Excelente", "timestamp": "2025-05-01 10:01"}
                ]
            },
            {
                "lead_id": "222",
                "mensagens": [
                    {"from": "lead", "text": "quero cancelar", "timestamp": "2025-05-01 11:00"}
                ]
            },
            {
                "lead_id": "333",
                "mensagens": [
                    {"from": "lead", "text": "preciso nota fiscal", "timestamp": "2025-05-01 12:00"}
                ]
            }
        ]

class TestDailyReportUnit(unittest.TestCase):
    def test_generate_report(self):
        # keywords_db mock
        keywords_file = "unit_test_keywords.json"
        import json
        db = {
            "agendamentos": ["vou agendar", "pode marcar"],
            "cancelamentos": ["cancelar", "desmarcar"],
            "pendencias_medico": ["nota fiscal", "pedido de exame"]
        }
        with open(keywords_file, "w", encoding="utf-8") as f:
            json.dump(db, f)

        fetcher = MockFetcher()
        report = DailyReport(fetcher=fetcher, keywords_file=keywords_file)
        resultado = report.generate_report()

        self.assertEqual(resultado["agendamentos_realizados"], 1)
        self.assertEqual(resultado["cancelamentos_consultas"], 1)
        self.assertEqual(resultado["pendencias_ao_medico"], 1)

        import os
        if os.path.exists(keywords_file):
            os.remove(keywords_file)

if __name__ == "__main__":
    unittest.main()
