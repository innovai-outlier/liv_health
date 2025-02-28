import streamlit as st
from .report import show_report
from .audit import show_audit
from .assistants import show_assistants

def show_dashboard():
    """ Exibe o painel principal com barra lateral de navegação """
    st.sidebar.title("🔍 Navegação")
    
    menu_options = {
        "👥 Assistentes": "assistants",
        "📊 Relatórios": "reports",
        "🔍 Auditoria": "audit",
        "🚪 Sair": "logout"
    }

    selection = st.sidebar.radio("Menu", list(menu_options.keys()))

    if selection == "👥 Assistentes":
        show_assistants()
    elif selection == "📊 Relatórios":
        show_report()
    elif selection == "🔍 Auditoria":
        show_audit()
    elif selection == "🚪 Sair":
        st.session_state.logout = True
