import os
import json
import glob
import tkinter as tk
import streamlit as st
from tkinter import Tk, filedialog
from abc import ABC, abstractmethod
from src.reports.chat_parser import parse_chat_file, extract_lead_id_from_folder  # Importação do parser

class ConversationsFetcher(ABC):
    """ Classe abstrata para padronizar a coleta de conversas. """

    @abstractmethod
    def fetch_today_conversations(self):
        """ Método abstrato para buscar as conversas do dia. """
        pass

class LocalFileFetcher(ConversationsFetcher):
    """
    Implementação que busca conversas da base local (database/)
    ou permite ao usuário selecionar um diretório contendo conversas individuais no modo produção.
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
        self.base_dir = None if base_type == "prod" else f"database/{base_type}/"

    def select_directory(self):
        """Abre um seletor de diretório no Streamlit via Tkinter"""
        root = Tk()
        root.withdraw()
        directory = filedialog.askdirectory(title="Selecione um diretório contendo conversas")
        root.destroy()
        return directory if directory else None

    def select_directory_streamlit(self):
        """
        Permite ao usuário selecionar um diretório via **entrada de texto** no Streamlit.
        Alternativamente, ele pode arrastar um arquivo do diretório para inferirmos o caminho.
        """

        st.warning("📂 **Digite o caminho do diretório ou arraste um arquivo de dentro dele para identificarmos automaticamente.**")

        # Opção 1: Entrada de texto para o caminho do diretório
        directory = st.text_input("📁 Caminho do Diretório", placeholder="Digite ou cole o caminho do diretório...")

        # Opção 2: Arrastar um arquivo do diretório desejado
        uploaded_file = st.file_uploader("📄 Ou selecione um arquivo qualquer do diretório desejado", type=["txt", "json"])

        # Se o usuário arrastou um arquivo, obtemos o diretório automaticamente
        if uploaded_file is not None:
            directory = os.path.dirname(uploaded_file.name)
            st.success(f"📁 Diretório detectado automaticamente: `{directory}`")

        # Bloqueia enquanto o diretório não for definido
        if not directory:
            st.warning("⚠️ Aguardando o usuário informar o diretório...")
            st.stop()

        return directory
    
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
        Carrega conversas de um dia específico dentro do diretório da base (train, test, validate, ou prod).
        Para bases `train/test/validate`: Lê JSONs diretos.
        Para `prod`: Processa arquivos `_chat.txt` dentro das pastas de lead.
        """
        all_conversations = []

        if not base_dir:
            print("⚠️ Caminho base_dir não especificado.")
            return []

        if self.base_type == "prod":
            # 📌 Busca todas as pastas no formato "WhatsApp Chat - *"
            folders = glob.glob(os.path.join(base_dir, "WhatsApp Chat - *"))
            
            for folder in folders:
                chat_file = os.path.join(folder, "_chat.txt")

                if os.path.exists(chat_file):
                    lead_id = extract_lead_id_from_folder(folder)
                    conv = parse_chat_file(chat_file, "", lead_id)  # 🔄 Sem rotulagem, apenas mensagens
                    all_conversations.append(conv)

        else:
            # 📌 Modo tradicional: Carrega JSONs da base de dados
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
                                filtered_messages = [
                                    msg for msg in conv["mensagens"] 
                                    if isinstance(msg, dict) and "timestamp" in msg and msg["timestamp"].startswith(str(target_date))
                                ]
                                
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
