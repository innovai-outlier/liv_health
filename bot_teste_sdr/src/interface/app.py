import streamlit as st
from auth import login_user
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.interface.dashboard import show_dashboard

# Tela de login
login_user()

if st.session_state['authentication_status']:
    st.sidebar.title(f"Bem-vindo, {st.session_state["name"]} 👋")
    show_dashboard()
elif st.session_state['authentication_status'] is False:
    st.error("⚠️ Usuário ou senha incorretos. Tente novamente.")
elif st.session_state['authentication_status'] is None:
    st.warning("🔑 Por favor, insira suas credenciais para acessar o sistema.")
