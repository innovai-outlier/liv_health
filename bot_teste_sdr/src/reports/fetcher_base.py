import os
import json
import tkinter as tk
from tkinter import filedialog
from abc import ABC, abstractmethod
from src.reports.chat_parser import parse_chat_file  # Importa o parser de conversas

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
    Implementação que busca conversas pré-processadas da base local (database/)
    ou permite ao usuário selecionar um diretório contendo arquivos de conversas.
    """

    def __init__(self, base_type="test"):
        """
        Inicializa o fetcher definindo a base de dados que será carregada.
        `base_type` pode ser:
          - "train" -> database/train/conversations.json
          - "test" -> database/test/conversations.json
          - "validate" -> database/validate/conversations.json
          - "prod" -> Abre uma caixa de diálogo para o usuário selecionar um diretório de conversas
        """
        self.base_type = base_type

        if base_type in ["train", "test", "validate"]:
            self.base_dir = f"database/{base_type}/"
            os.makedirs(self.base_dir, exist_ok=True)  # Garante que a pasta exista
        elif base_type == "prod":
            self.base_dir = self.select_directory()  # Usuário escolhe a pasta
        else:
            raise ValueError("base_type inválido. Escolha entre 'train', 'test', 'validate' ou 'prod'.")

    def select_directory(self):
        """ Abre um seletor para o usuário escolher um diretório contendo conversas. """
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal do Tkinter
        directory = filedialog.askdirectory(title="Selecione um diretório contendo conversas")
        return directory if directory else None  # Retorna o caminho ou None caso o usuário cancele

    def fetch_today_conversations(self, target_date="2025-01-02"):
        """
        Carrega as conversas usando `load_conversations()`, independentemente do tipo de base.
        """
        if not self.base_dir or not os.path.exists(self.base_dir):
            print(f"⚠️ Diretório de conversas inválido ou não selecionado: {self.base_dir}")
            return []

        # Chama a função load_conversations() para carregar as conversas processadas
        return self.load_conversations(base_dir=self.base_dir, target_date=target_date)

    def load_conversations(self, base_dir, target_date="2025-01-02"):
        """
        Carrega conversas de um dia específico dentro do diretório da base (train, test ou validate).
        Retorna apenas conversas onde há pelo menos uma mensagem registrada na data desejada.
        """
        all_conversations = []
        if not base_dir:
            print("⚠️ Caminho base_dir não especificado.")
            return []

        for file in os.listdir(base_dir):
            if file.endswith(".json"):
                file_path = os.path.join(base_dir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)  # Agora sabemos que data é uma lista!

                        # Verifica se o JSON contém uma lista de conversas
                        if not isinstance(data, list):
                            print(f"⚠️ ERRO: Estrutura inesperada no arquivo {file}. Esperado uma lista de conversas, mas recebeu {type(data)}.")
                            continue

                        # Itera sobre cada conversa na lista
                        for conv in data:
                            if not isinstance(conv, dict):
                                print(f"⚠️ ERRO: Conversa mal formatada no arquivo {file}: esperado dicionário, mas recebeu {type(conv)}.")
                                continue

                            if "mensagens" not in conv or not isinstance(conv["mensagens"], list):
                                print(f"⚠️ ERRO: Estrutura incorreta em {file}. Conversa sem 'mensagens' ou formato inesperado.")
                                continue

                            # 🔍 Filtra mensagens do dia desejado
                            filtered_messages = [msg for msg in conv["mensagens"] if isinstance(msg, dict) and "timestamp" in msg and msg["timestamp"].startswith(str(target_date))]
                            
                            # Apenas adiciona conversas que tenham mensagens no dia filtrado
                            if filtered_messages:
                                all_conversations.append({
                                    "lead_id": conv.get("lead_id", "desconhecido"),  # Mantém lead_id
                                    "label": conv.get("label", "desconhecido"),  # Mantém rótulo
                                    "mensagens": filtered_messages
                                })

                    except json.JSONDecodeError as e:
                        print(f"⚠️ ERRO: Falha ao decodificar JSON em {file}: {e}")

        print(f"✅ {len(all_conversations)} conversas carregadas para {target_date}.")
        return all_conversations
