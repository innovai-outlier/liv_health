import streamlit as st
import json
import os
from utils import carregar_json

# Caminho da base de assistentes (simulada)
ASSISTANTS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "assistants.json")

def carregar_assistentes():
    """ Carrega lista de assistentes disponíveis """
    return carregar_json(ASSISTANTS_FILE) or []

def show_assistants():
    """ Exibe painel de assistentes do usuário """
    st.title("👥 Assistentes Sob Seu Controle")

    assistentes = carregar_assistentes()

    if not assistentes:
        st.warning("⚠️ Nenhuma assistente encontrada.")
        return

    col1, col2 = st.columns(2)

    for i, assistente in enumerate(assistentes):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(f"🆔 {assistente['nome']}", key=f"btn_{assistente['id']}"):
                exibir_detalhes_assistente(assistente)

def exibir_detalhes_assistente(assistente):
    """ Exibe um popup com informações detalhadas da assistente """
    with st.expander(f"📌 Informações de {assistente['nome']}"):
        st.markdown(f"""
        - **Nome:** {assistente['nome']}
        - **Categoria:** {assistente['categoria']}
        - **Número do WhatsApp Business:** {assistente['numero_wab']}
        - **Criada em:** {assistente['data_criacao']}
        - **Status:** {"🟢 Ativa" if assistente['ativa'] else "🔴 Inativa"}
        """)

        if st.button("✏️ Editar", key=f"edit_{assistente['id']}"):
            st.info("🚧 Funcionalidade de edição em desenvolvimento...")

        if st.button("🗑️ Remover", key=f"del_{assistente['id']}"):
            st.warning("⚠️ Tem certeza que deseja remover esta assistente?")
