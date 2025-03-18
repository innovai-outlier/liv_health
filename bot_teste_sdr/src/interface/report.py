import streamlit as st
import json
import os, sys, time
from datetime import datetime
from utils import carregar_json
import re
import pandas as pd
from src.reports.fetcher_base import LocalFileFetcher
from fpdf import FPDF

# 🔹 Adiciona "src" ao caminho de pacotes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# Agora importe o módulo corretamente
import src.reports.workflow_reports as wfr


ASSISTANTS_FILE = os.path.join(os.path.dirname(__file__), "data", "assistants.json")

# Diretório correto da pasta "output" na raiz do projeto
OUTPUT_DIR = os.path.abspath(os.path.join(os.getcwd(), "output"))

# Importa relatório para um, arquivo PDF
def generate_pdf(assistente_nome, categoria, numero_wab, data_analise, metricas_extraidas):
    """
    Gera um PDF estilizado com as informações do relatório.
    """

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # 🔵 Definir estilos do PDF
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(30, 144, 255)  # Azul escuro
    pdf.cell(200, 10, "📊 Relatório Diário de Conversas", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)  # Preto
    pdf.cell(200, 10, f"Data da Análise: {data_analise.strftime('%d/%m/%Y')}", ln=True, align="C")
    pdf.ln(10)

    # 🔹 Informações Gerais
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(30, 144, 255)  # Azul escuro
    pdf.cell(200, 10, "📌 Informações Gerais", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, f"🔹 Assistente: {assistente_nome}\n"
                          f"🔹 Categoria: {categoria}\n"
                          f"🔹 Contato WAB: {numero_wab}\n")
    pdf.ln(5)

    # 🔎 Insights das Conversas
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(30, 144, 255)
    pdf.cell(200, 10, "🔎 Insights das Conversas", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)

    for chave, valor in metricas_extraidas.items():
        if isinstance(valor, list):
            valor = ", ".join(valor) if valor else "Nenhum"
        pdf.cell(0, 8, f"🔹 {chave}: {valor}", ln=True)

    pdf.ln(10)

    # 📂 Salvar o PDF temporariamente
    pdf_filename = f"relatorio_{assistente_nome}_{data_analise.strftime('%d-%m-%Y')}.pdf"
    pdf_path = os.path.join("output", pdf_filename)

    os.makedirs("output", exist_ok=True)
    pdf.output(pdf_path)

    return pdf_path

# Carregar assistentes disponíveis
def carregar_assistentes():
    """ Retorna a lista de assistentes cadastradas no sistema. """
    #assistentes_file = "data/assistentes.json"  # Arquivo com assistentes registradas
    if os.path.exists(ASSISTANTS_FILE):
        assist_json = carregar_json(ASSISTANTS_FILE)
        return [assistente.get('nome') for assistente in assist_json if 'nome' in assistente]
    return []

def extrair_metricas(relatorio):
    """Extrai as métricas do relatório diretamente do JSON estruturado."""
    
    origem_atendimento = relatorio.get("origem_atendimento", {})

    metricas = {
        "Quantidade de agendamentos": relatorio.get("quantidade_agendamentos", 0),
        "Google": relatorio.get("origem_atendimento", {}).get("Google", None),
        "Instagram": relatorio.get("origem_atendimento", {}).get("Instagram", None),
        "Indicação": relatorio.get("origem_atendimento", {}).get("Indicação", None),
        "Já é paciente": relatorio.get("origem_atendimento", {}).get("Já é paciente", None),
        "Cancelamentos": relatorio.get("cancelamentos", 0),
        "Motivo do cancelamento": relatorio.get("motivos_cancelamento", {}),
        "Reagendamentos": relatorio.get("reagendamentos", 0),
        "Motivo do reagendamento": relatorio.get("motivos_reagendamento", {}),
        "Leads sem atendimento": relatorio.get("leads_sem_atendimento", []),
        "Leads inertes": relatorio.get("leads_inertes", []),
        "Pendências ao médico": relatorio.get("pendencias_ao_medico", {}),
        "Tempo máximo de resposta": relatorio.get("tempo_maximo_resposta", {})
    }
    
    return metricas

def show_report():
    """ Exibe a tela do relatório diário """
    st.title("📊 Relatório Diário de Conversas")
    st.markdown("🚀 **Produzido por:** INNOVAI (BETA VERSION)")
    
    # Carregar assistentes cadastradas
    assistentes_disponiveis = carregar_assistentes()
    
    # Formulário antes da exibição do relatório
    with st.form("form_relatorio"):
        assistente_nome = st.selectbox("Selecione a Assistente...", assistentes_disponiveis)
        categoria = st.selectbox("Categoria", ["Humana", "IA"])
        numero_wab = st.text_input("Número do WhatsApp Business", "+55 11 99999-9999")
        data_analise = st.date_input("Data da Análise", datetime.today())

        # Criando o Fetcher e aguardando o usuário escolher um diretório
        fetcher = LocalFileFetcher(base_type="prod")
        btn_gerar_relatorio = st.form_submit_button("🔍 Gerar Relatório")
        
    if btn_gerar_relatorio:
        REPORT_FILENAME = f"{assistente_nome}_{data_analise}_report.json"
        REPORT_PATH = os.path.join(OUTPUT_DIR, REPORT_FILENAME)
        with st.spinner("⏳ Processando relatório..."):
            if numero_wab == "+55 11 99999-9999": #Executa Output Ideal do Modelo GPT-4o
                REPORT_FILENAME = "GPT_EXPECTED_OUTPUT.json"
                REPORT_PATH = os.path.join(OUTPUT_DIR, REPORT_FILENAME)
                wfr.generate_report(showtime=True) #Modo exibição
            else:
                selected_dir = fetcher.select_directory()
                if selected_dir:
                    st.session_state.selected_directory = selected_dir
                    #st.success(f"📂 Diretório ativo: {selected_dir}")
                    
                 # Verifica se o usuário selecionou um diretório
                if "selected_directory" not in st.session_state or not st.session_state.selected_directory:
                    st.warning("⚠️ Nenhum diretório selecionado. Escolha um antes de prosseguir.")
                    return
                
                st.success(f"📂 Diretório carregado: {st.session_state.selected_directory}")

                # Atualiza o caminho da base para o fetcher
                fetcher.base_dir = st.session_state.selected_directory
                
                conversations = fetcher.fetch_today_conversations(target_date=data_analise)
                wfr.generate_report(target_date=data_analise, 
                                    assistente=assistente_nome, 
                                    base_type='prod', 
                                    conversations=conversations)  # Chama a geração do relatório
            time.sleep(2)  # Simula tempo de processamento
            
        st.success("✅ Relatório gerado com sucesso!")
        
        relatorio = carregar_json(REPORT_PATH)
        if not relatorio:
            st.error("⚠️ Nenhum relatório encontrado. Execute a geração primeiro.")  
            return
        
        # 🔎 Insights Gerais
        st.markdown("---")
        st.subheader("🔎 Insights das Conversas")
        
        metricas = extrair_metricas(relatorio["resumo"])
        
        col_ag, col_can, col_reag = st.columns(3)
        
        with col_ag:
            st.metric(label="📅 Agendamentos", value=metricas.get("Quantidade de agendamentos"))
        
        with col_can:
            st.metric(label="📉 Cancelamentos", value=metricas.get("Cancelamentos"))
            
        with col_reag:
            st.metric(label="📌 Reagendamentos", value=metricas.get("Reagendamentos"))
        
        # Origem dos atendimentos
        st.markdown("---")
        st.subheader("📊 Origem dos Agendamentos")
        # Exibe a origem dos atendimentos em ordem decrescente de percentual
        total_agendamentos = int(metricas.get("Quantidade de agendamentos", 0))

        if total_agendamentos == 0:
            st.warning("⚠️ Nenhum agendamento encontrado. Exibindo apenas os valores absolutos.")
        else:
            # Criar lista de origem com seus respectivos percentuais
            origens = [
                (origem, int(valor), (int(valor) / total_agendamentos) * 100 if total_agendamentos > 0 else 0)
                for origem, valor in metricas.items()
                    if origem in ['Google', 'Instagram', 'Indicação', 'Já é paciente']
            ]

            # Ordenar a lista por percentual em ordem decrescente
            origens = sorted(origens, key=lambda x: x[2], reverse=True)

            # Exibir os valores na ordem correta
            for origem, valor, percentual in origens:
                st.write(f"🔹 **{origem}:** {valor} ({percentual:.1f}%)")
                st.progress(percentual / 100)

        # Tempo máximo de resposta
        st.markdown("---")
        st.subheader("⏳ Tempo Máximo de Resposta")
        for lead, tempo in metricas.get("Tempo máximo de resposta").items():
            st.write(f"🕒 **{lead}:** {tempo}")

        # Pendências ao médico
        st.markdown("---")
        st.subheader("⚕️ Pendências Médicas")
        pendencias_medico = metricas.get("Pendências ao médico")
        
        if pendencias_medico:
            for lead, pendencia in metricas.get("Pendências ao médico").items():
                st.write(f"📌 **{lead}:** {pendencia}")
        else:
            st.success("✅ Nenhuma pendência encontrada.")
        
        # 🔴 Motivos de Cancelamento
        st.markdown("---")
        st.subheader("❌ Motivos de Cancelamento")

        motivos_cancelamento = metricas.get("Motivo do cancelamento", {})

        if motivos_cancelamento:
            for lead, motivo in motivos_cancelamento.items():
                st.write(f"📌 **{lead}** - {motivo}")
        else:
            st.success("✅ Nenhum cancelamento registrado.")

        # 🔵 Motivos de Reagendamento
        st.markdown("---")
        st.subheader("📅 Motivos de Reagendamento")

        motivos_reagendamento = metricas.get("Motivo do reagendamento", {})

        if motivos_reagendamento:
            for lead, motivo in motivos_reagendamento.items():
                st.write(f"🔄 **{lead}** - {motivo}")
        else:
            st.success("✅ Nenhum reagendamento registrado.")
        
        
         # 📥 Botão para gerar PDF
        if st.button("📥 Baixar Relatório em PDF"):
            pdf_path = generate_pdf(assistente_nome, categoria, numero_wab, data_analise, relatorio)
            print(pdf_path)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(label="📄 Baixar PDF", data=pdf_file, file_name=os.path.basename(pdf_path), mime="application/pdf")

        ##st.markdown("---")
        # 💬 Conversas na Íntegra
        ##st.subheader("💬 Conversas na Íntegra")
        ##if "mostrar_conversas" not in st.session_state:
        ##    st.session_state.mostrar_conversas = False

        ##if st.button("👁️ Exibir Conversas" if not st.session_state.mostrar_conversas else "🙈 Ocultar Conversas"):
        ##    st.session_state.mostrar_conversas = not st.session_state.mostrar_conversas

        ##if st.session_state.mostrar_conversas:
        ##    st.text_area("📜 Histórico Completo", relatorio["resumo"], height=400)
