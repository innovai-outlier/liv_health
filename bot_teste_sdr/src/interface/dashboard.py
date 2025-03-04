import streamlit as st
from .report import show_report
from .audit import show_audit
from .assistants import show_assistants
from streamlit_option_menu import option_menu


def show_dashboard():
    """ Exibe o painel principal com menu lateral estilizado. """

    # Definir estilos customizados para o painel lateral
    sidebar_style = """
        <style>
            [data-testid="stSidebar"] {
                background-color: #2c3e50;  /* Cor mais escura */
            }
            .css-10trblm {
                font-size: 18px !important; /* Ajusta o tamanho dos ícones */
            }
        </style>
    """
    st.markdown(sidebar_style, unsafe_allow_html=True)

    # Criar menu lateral estilizado com ícones maiores
    with st.sidebar:
        menu_selecao = option_menu(
            menu_title="Menu Principal",
            options=["Assistentes", "Relatórios", "Auditorias", "Sair"],
            icons=["person-circle", "clipboard-data", "shield-lock", "box-arrow-right"],
            menu_icon="cast",
            default_index=1,
            styles={
                "container": {"padding": "5px", "background-color": "#000000"},
                "icon": {"color": "white", "font-size": "22px"},
                "nav-link": {"font-size": "18px", "text-align": "left", "margin": "5px"},
                "nav-link-selected": {"background-color": "#1abc9c"},
            }
        )

    # Direcionar para a funcionalidade escolhida
    if menu_selecao == "Assistentes":
        st.subheader("👩‍💼 Gerenciamento de Assistentes")
        st.write("Aqui você pode visualizar e gerenciar as assistentes cadastradas.")
        show_assistants()
    elif menu_selecao == "Relatórios":
        show_report()
    elif menu_selecao == "Auditorias":
        st.subheader("🛡️ Auditoria de Assistentes")
        st.write("Ferramenta para verificar a performance das assistentes.")
        audit()
    elif menu_selecao == "Sair":
        st.subheader("🔒 Logout")
        st.write("Você foi desconectado.")

def show_dashboard_old():
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
