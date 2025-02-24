# src/reports/fetcher_api.py
import requests
from .fetcher_base import ConversationsFetcher

class APIConversationsFetcher(ConversationsFetcher):
    """
    Exemplo de fetcher usando API (mock).
    """

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def fetch_today_conversations(self):
        # TODO: Implementar requisição real
        return [
            {
                "lead_id": "999-8888",
                "mensagens": [
                    {"from": "lead", "text": "quero cancelar", "timestamp": "2025-05-02 10:00"},
                    {"from": "assistente", "text": "certo, posso saber o motivo?", "timestamp": "2025-05-02 10:01"}
                ],
                "timestamp": "2025-05-02 10:00"
            }
        ]
