# src/reports/fetcher_selenium.py
from .fetcher_base import ConversationsFetcher

class SeleniumConversationsFetcher(ConversationsFetcher):
    """
    Exemplo de fetcher usando Selenium 
    (neste exemplo simplificado, retornamos mock)
    """

    def __init__(self, driver_path, url):
        self.driver_path = driver_path
        self.url = url

    def fetch_today_conversations(self):
        # TODO: Implementar Selenium real
        return [
            {
                "lead_id": "555-1111",
                "mensagens": [
                    {"from": "lead", "text": "vou agendar hoje", "timestamp": "2025-05-02 09:00"},
                    {"from": "assistente", "text": "ótimo!", "timestamp": "2025-05-02 09:01"}
                ],
                "timestamp": "2025-05-02 09:00"
            }
        ]
