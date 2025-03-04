import streamlit as st
import json
import os

# Caminho correto para o relatório gerado pelo modelo
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Diretório atual (src/interface)
REPORT_FILE = "output/test_report.json"
def carregar_relatorio():
    """ Carrega o relatório gerado pela IA, verificando se o arquivo existe """
    if not os.path.exists(REPORT_FILE):
        return {"resumo": "⚠️ Nenhum relatório encontrado. Execute a geração do relatório primeiro."}
    
    with open(REPORT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# Criar interface do relatório
st.set_page_config(page_title="Relatório Diário de Conversas", layout="wide")

# Carregar dados
relatorio = carregar_relatorio()

# Cabeçalho principal
st.title("📊 Relatório Diário de Conversas")
st.markdown("🚀 **Produzido por:** INNOVAI")

# **Sessão Geral**
st.subheader("📌 Informações Gerais")
st.markdown(f"""
- **Assistente:** 
- **Categoria:** Inteligência Artificial  
- **Data da Análise:** 02/01/2025
- **Contato da Assistente:** +55(11)944885013  
""")

# **Sessão de Métricas**
st.subheader("📊 Métricas")

metrica_texto = relatorio.get("resumo", "").split("--------------------------------------------------")

if len(metrica_texto) > 2:
    metricas = metrica_texto[2].strip().split("\n")
    metricas_formatadas = {}
    
    for metrica in metricas:
        if ":" in metrica:
            chave, valor = metrica.split(":")
            metricas_formatadas[chave.strip()] = valor.strip()

    # Exibir métricas em tabela
    st.table(metricas_formatadas)
else:
    st.warning("⚠️ Nenhuma métrica encontrada no relatório.")

# **Sessão de Conversas**
st.subheader("💬 Conversas")

# Adicionar botão para exibir/ocultar conversas
if "mostrar_conversas" not in st.session_state:
    st.session_state.mostrar_conversas = False

if st.button("👁️ Exibir Conversas" if not st.session_state.mostrar_conversas else "🙈 Ocultar Conversas"):
    st.session_state.mostrar_conversas = not st.session_state.mostrar_conversas

# Exibir conversas se o usuário clicar no botão
if st.session_state.mostrar_conversas:
    st.text_area("Detalhes das Conversas", relatorio.get("resumo", "Nenhuma conversa encontrada"), height=300)

# Rodar com `streamlit run src/interface/app.py`
