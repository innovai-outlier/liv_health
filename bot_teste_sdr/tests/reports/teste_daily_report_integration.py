# tests/reports/test_daily_report_integration.py
import unittest
from src.reports.fetcher_selenium import SeleniumConversationsFetcher
from src.reports.fetcher_api import APIConversationsFetcher
from src.reports.daily_report import DailyReport
import json
import os

class TestDailyReportIntegration(unittest.TestCase):
    def setUp(self):
        self.keywords_file = "integration_test_keywords.json"
        db = {
            "agendamentos": ["vou agendar", "pode marcar"],
            "cancelamentos": ["cancelar", "desmarcar"],
            "pendencias_medico": ["nota fiscal", "pedido de exame"]
        }
        with open(self.keywords_file, "w", encoding="utf-8") as f:
            json.dump(db, f)

    def tearDown(self):
        if os.path.exists(self.keywords_file):
            os.remove(self.keywords_file)

    def test_selenium_fetcher_integration(self):
        fetcher = SeleniumConversationsFetcher(driver_path="dummy", url="dummy")
        dr = DailyReport(fetcher=fetcher, keywords_file=self.keywords_file)
        result = dr.generate_report()
        # Checar se retornou algo
        self.assertIn("agendamentos_realizados", result)

    def test_api_fetcher_integration(self):
        fetcher = APIConversationsFetcher(base_url="http://example.com", token="abc123")
        dr = DailyReport(fetcher=fetcher, keywords_file=self.keywords_file)
        result = dr.generate_report()
        self.assertIn("cancelamentos_consultas", result)

if __name__ == "__main__":
    unittest.main()
