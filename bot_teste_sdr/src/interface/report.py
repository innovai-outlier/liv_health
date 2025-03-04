import streamlit as st
import json
import os, sys
from datetime import datetime
from utils import carregar_json
import re
import pandas as pd

# 🔹 Adiciona "src" ao caminho de pacotes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# Agora importe o módulo corretamente
import src.reports.workflow_reports as wfr


ASSISTANTS_FILE = os.path.join(os.path.dirname(__file__), "data", "assistants.json")

# Diretório correto da pasta "output" na raiz do projeto
OUTPUT_DIR = os.path.abspath(os.path.join(os.getcwd(), "output"))

def exibir_tabela_formatada(metricas_extraidas):
    """ Exibe a tabela de insights formatada em Streamlit """

    # Converter dicionário para DataFrame
    df = pd.DataFrame(list(metricas_extraidas.items()), columns=["Métrica", "Valor"])

    # Aplicando um CSS para estilizar a tabela
    st.markdown("""
        <style>
        .stDataFrame {
            background-color: #fdfdfd;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        table tbody tr:hover {
            background-color: #f0f0f0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Exibir tabela
    st.dataframe(df, use_container_width=True)

def extrair_metricas(texto):
    """ Extrai as métricas do relatório usando expressões regulares """
    padroes = {
        "Quantidade de agendamentos": r"Quantidade de agendamentos:\s*(\d+)",
        "Google": r"-\s*(\d+)\s*Google",
        "Instagram": r"-\s*(\d+)\s*Instagram",
        "Indicação": r"-\s*(\d+)\s*Indicação",
        "Cancelamentos": r"Cancelamentos:\s*(\d+)",
        "Motivo do cancelamento": r"Motivo:\s*(.*)",
        "Reagendamentos": r"Reagendamentos:\s*(\d+)",
        "Motivo do reagendamento": r"Motivo:\s*(.*)",
        "Conversas em aberto (Assistente não respondeu)": r"Conversas em aberto \(Assistente não respondeu\):\s*(\d+)",
        "Conversas em aberto (Lead não respondeu)": r"Conversas em aberto \(Lead não respondeu\):\s*(\d+)"
    }
    
    metricas = {}
    for chave, padrao in padroes.items():
        match = re.search(padrao, texto)
        metricas[chave] = match.group(1) if match else "Não informado"
    
    return metricas

def extrair_pendencias(texto):
    """ Extrai as pendências ao médico do relatório """
    padrao_pendencias = r"- ID do lead: (\d+-\d+)\n\s*- Pendência: (.+)"
    pendencias = re.findall(padrao_pendencias, texto)
    return pendencias if pendencias else [("Nenhuma", "Não informado")]

# Carregar assistentes disponíveis
def carregar_assistentes():
    """ Retorna a lista de assistentes cadastradas no sistema. """
    #assistentes_file = "data/assistentes.json"  # Arquivo com assistentes registradas
    if os.path.exists(ASSISTANTS_FILE):
        assist_json = carregar_json(ASSISTANTS_FILE)
        return [assistente.get('nome') for assistente in assist_json if 'nome' in assistente]
    return []

def show_report():
    """ Exibe a tela do relatório diário """
    st.title("📊 Relatório Diário de Conversas")
    st.markdown("🚀 **Produzido por:** INNOVAI")
    
    # Carregar assistentes cadastradas
    assistentes_disponiveis = carregar_assistentes()
    
    # Formulário antes da exibição do relatório
    
    with st.form("form_relatorio"):
        assistente_nome = st.selectbox("Selecione a Assistente...", assistentes_disponiveis)
        categoria = st.selectbox("Categoria", ["Humana", "IA"])
        numero_wab = st.text_input("Número do WhatsApp Business", "+55 11 99999-9999")
        data_analise = st.date_input("Data da Análise", datetime.today())

        submit_button = st.form_submit_button("🔍 Gerar Relatório")

    if submit_button:
        REPORT_FILENAME = f"{assistente_nome}_{data_analise}_report.json"
        REPORT_PATH = os.path.join(OUTPUT_DIR, REPORT_FILENAME)
        with st.spinner("⏳ Processando relatório..."):
            wfr.generate_report(target_date=data_analise, assistente=assistente_nome)  # Chama a geração do relatório
            time.sleep(2)  # Simula tempo de processamento
            
        st.success("✅ Relatório gerado com sucesso!")
        
        relatorio = carregar_json(REPORT_PATH)
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

        # 🔎 Insights
        st.subheader("🔎 Insights das Conversas")
        metricas_extraidas = extrair_metricas(relatorio["resumo"])
        exibir_tabela_formatada(metricas_extraidas)

        # 🌟 Destaques Relevantes
        st.subheader("🌟 Destaques Relevantes")
        pendencias_extraidas = extrair_pendencias(relatorio["resumo"])
        for lead_id, pendencia in pendencias_extraidas:
            st.write(f"📌 **{lead_id}** - {pendencia}")

        # 💬 Conversas na Íntegra
        st.subheader("💬 Conversas na Íntegra")
        if "mostrar_conversas" not in st.session_state:
            st.session_state.mostrar_conversas = False

        if st.button("👁️ Exibir Conversas" if not st.session_state.mostrar_conversas else "🙈 Ocultar Conversas"):
            st.session_state.mostrar_conversas = not st.session_state.mostrar_conversas

        if st.session_state.mostrar_conversas:
            st.text_area("📜 Histórico Completo", relatorio["resumo"], height=400)
