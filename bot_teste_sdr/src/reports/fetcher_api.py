# src/reports/fetcher_api.py
import requests
from .fetcher_base import ConversationsFetcher

class APIConversationsFetcher(ConversationsFetcher):
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def fetch_today_conversations(self):
        # TODO: requisição real
        # Exemplo: mock
        return [
            {
                "lead_id": "api_mock_lead",
                "mensagens": [
                    {"from": "lead", "text": "quero cancelar", "timestamp": "2025-05-01 11:00"},
                    {"from": "assistente", "text": "Tudo bem, qual o motivo?", "timestamp": "2025-05-01 11:01"}
                ]
            }
        ]
