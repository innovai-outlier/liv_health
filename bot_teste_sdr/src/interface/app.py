import streamlit as st
from auth import login_user
from dashboard import show_dashboard


# Tela de login
login_user()

if st.session_state['authentication_status']:
    st.sidebar.title(f"Bem-vindo, {st.session_state["name"]} 👋")
    show_dashboard()
elif st.session_state['authentication_status'] is False:
    st.error("⚠️ Usuário ou senha incorretos. Tente novamente.")
elif st.session_state['authentication_status'] is None:
    st.warning("🔑 Por favor, insira suas credenciais para acessar o sistema.")
