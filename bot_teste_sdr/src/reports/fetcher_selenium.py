# src/reports/fetcher_selenium.py
from .fetcher_base import ConversationsFetcher

class SeleniumConversationsFetcher(ConversationsFetcher):
    def __init__(self, driver_path, url):
        self.driver_path = driver_path
        self.url = url

    def fetch_today_conversations(self):
        # TODO: Implementar Selenium real
        # Exemplo: Retorna mock
        return [
            {
                "lead_id": "selenium_mock_lead",
                "mensagens": [
                    {"from": "lead", "text": "vou agendar agora", "timestamp": "2025-05-01 10:00"},
                    {"from": "assistente", "text": "Perfeito", "timestamp": "2025-05-01 10:01"}
                ]
            }
        ]
