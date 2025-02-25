# src/reports/fetcher_base.py
from abc import ABC, abstractmethod

class ConversationsFetcher(ABC):
    @abstractmethod
    def fetch_today_conversations(self):
        """
        Retorna lista de conversas:
        [
          {
            "lead_id": "...",
            "mensagens": [
               {"from": "lead"/"assistente", "text": "...", "timestamp": "..."},
               ...
            ]
          },
          ...
        ]
        """
        pass
