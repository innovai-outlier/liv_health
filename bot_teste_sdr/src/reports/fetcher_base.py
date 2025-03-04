import os
import json
from abc import ABC, abstractmethod

class ConversationsFetcher(ABC):
    """
    Classe abstrata para padronizar a coleta de conversas.
    Pode ser implementada para diferentes fontes: Selenium, API, Arquivo Local.
    """

    @abstractmethod
    def fetch_today_conversations(self):
        """
        Método abstrato para buscar as conversas do dia.
        Cada implementação deve definir como as conversas são coletadas.
        """
        pass

class LocalFileFetcher(ConversationsFetcher):
    """
    Implementação que busca conversas pré-processadas da base local (database/).
    """

    def __init__(self, base_type="test"):
        """
        Inicializa o fetcher definindo a base de dados que será carregada.
        `base_type` pode ser: "train", "test" ou "validate".
        """
        self.base_type = base_type
        self.file_path = f"database/{base_type}/conversations.json"

    def fetch_today_conversations(self):
        """
        Carrega o arquivo JSON correspondente à base escolhida.
        """
        if not os.path.exists(self.file_path):
            print(f"⚠️ Arquivo de conversas não encontrado: {self.file_path}")
            return []

        with open(self.file_path, "r", encoding="utf-8") as f:
            conversations = json.load(f)

        print(f"✅ {len(conversations)} conversas carregadas de {self.file_path}")
        return conversations
