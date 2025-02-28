import streamlit as st
from auth import login_user
from dashboard import show_dashboard

# Tela de login
name, authentication_status, username = login_user()

if authentication_status:
    st.sidebar.title(f"Bem-vindo, {name} 👋")
    show_dashboard()
elif authentication_status is False:
    st.error("⚠️ Usuário ou senha incorretos. Tente novamente.")
elif authentication_status is None:
    st.warning("🔑 Por favor, insira suas credenciais para acessar o sistema.")
