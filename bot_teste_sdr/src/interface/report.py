import streamlit as st
import json
import os
from datetime import datetime
from utils import carregar_json

# Caminho do relatório
REPORT_FILE = os.path.join(os.path.dirname(__file__), "..", "reports", "output", "daily_report.json")

def show_report():
    """ Exibe a tela do relatório diário """
    st.title("📊 Relatório Diário de Conversas")
    st.markdown("🚀 **Produzido por:** INNOVAI")

    # Formulário antes da exibição do relatório
    with st.form("form_relatorio"):
        assistente_nome = st.text_input("Nome da Assistente", "IA Generativa")
        categoria = st.selectbox("Categoria", ["Humana", "IA"])
        numero_wab = st.text_input("Número do WhatsApp Business", "+55 11 99999-9999")
        data_analise = st.date_input("Data da Análise", datetime.today())

        submit_button = st.form_submit_button("🔍 Gerar Relatório")

    if submit_button:
        relatorio = carregar_json(REPORT_FILE)
        
        if not relatorio:
            st.error("⚠️ Nenhum relatório encontrado. Execute a geração primeiro.")
            return
        
        # Informações Gerais
        st.subheader("📌 Informações Gerais")
        st.markdown(f"""
        - **Assistente:** {assistente_nome}  
        - **Categoria:** {categoria}  
        - **Contato WAB:** {numero_wab}  
        - **Data da Análise:** {data_analise.strftime("%d/%m/%Y")}  
        """)

        # Insights
        st.subheader("🔎 Insights das Conversas")
        insights_texto = relatorio.get("resumo", "").split("Parte 1: Resumo Analítico")
        if len(insights_texto) > 1:
            insights_lista = insights_texto[1].strip().split("\n")
            insights_formatados = {chave.strip(): valor.strip() for item in insights_lista if ":" in item for chave, valor in [item.split(":")]}
            st.table(insights_formatados)
        else:
            st.warning("⚠️ Nenhum insight encontrado no relatório.")

        # Destaques
        st.subheader("🌟 Destaques Relevantes")
        detalhes_texto = relatorio.get("resumo", "").split("Parte 2: Resumo Detalhado")
        if len(detalhes_texto) > 1:
            st.write("\n".join(detalhes_texto[1].strip().split("\n")))
        else:
            st.warning("⚠️ Nenhuma informação detalhada encontrada.")

        # Conversas
        st.subheader("💬 Conversas na Íntegra")
        if "mostrar_conversas" not in st.session_state:
            st.session_state.mostrar_conversas = False

        if st.button("👁️ Exibir Conversas" if not st.session_state.mostrar_conversas else "🙈 Ocultar Conversas"):
            st.session_state.mostrar_conversas = not st.session_state.mostrar_conversas

        if st.session_state.mostrar_conversas:
            conversa_formatada = relatorio.get("resumo", "").split("Considere todas as interações abaixo para compilar seu relatório.")
            if len(conversa_formatada) > 1:
                st.text_area("📜 Histórico Completo", conversa_formatada[1].strip(), height=400)
            else:
                st.warning("⚠️ Nenhuma conversa detalhada encontrada.")
