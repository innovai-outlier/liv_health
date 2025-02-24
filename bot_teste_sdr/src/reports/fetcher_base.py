# src/reports/fetcher_base.py
from abc import ABC, abstractmethod

class ConversationsFetcher(ABC):
    """
    Interface para coleta das conversas diárias, 
    independentemente da origem (Selenium ou API).
    """

    @abstractmethod
    def fetch_today_conversations(self):
        """
        Retorna lista de conversas do dia no formato:
        [
          {
            "lead_id": "...",
            "mensagens": [
              {"from": "lead"/"assistente", "text": "...", "timestamp": "..."},
              ...
            ],
            "timestamp": "..."
          },
          ...
        ]
        """
        pass
