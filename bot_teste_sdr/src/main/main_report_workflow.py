import os
import json
import time
import argparse
from src.reports.daily_report import DailyReport
from src.reports.fetcher_base import ConversationsFetcher
from src.reports.fetcher_api import APIConversationsFetcher  # Futuro
from src.reports.fetcher_selenium import SeleniumConversationsFetcher  # TODO
from src.reports.apply_feedback import aplicar_feedback

# Caminhos dos arquivos de saída
REPORT_PATH = "output/daily_report.json"
FEEDBACK_PATH = "output/feedback.json"

class LocalFileFetcher(ConversationsFetcher):
    """ Fetcher que carrega conversas do chatbase local """
    def fetch_today_conversations(self):
        from src.reports.chat_parser import load_labeled_history
        return load_labeled_history(base_dir="assets/chatbase/")

def save_feedback_template():
    """ Gera um template de feedback para preenchimento manual """
    feedback_data = {
        "status": "pending",
        "comentarios": "",
        "correcoes": []
    }
    with open(FEEDBACK_PATH, "w", encoding="utf-8") as f:
        json.dump(feedback_data, f, indent=4, ensure_ascii=False)
    print(f"🔹 Feedback template gerado em {FEEDBACK_PATH}")

def wait_for_feedback():
    """ Aguarda o feedback humano ser preenchido """
    print("⏳ Aguardando o feedback manual...")
    while True:
        if os.path.exists(FEEDBACK_PATH):
            with open(FEEDBACK_PATH, "r", encoding="utf-8") as f:
                feedback_data = json.load(f)
                if feedback_data.get("status") == "approved":
                    print("✅ Feedback aprovado! Aplicando aprendizado...")
                    return feedback_data
        time.sleep(30)  # Aguarda 30 segundos antes de verificar novamente

def run_workflow(mode="estatico"):
    """ Executa o fluxo de geração de relatórios e permite ativação opcional do feedback """

    print(f"🚀 Iniciando workflow no modo: {mode.upper()}")

    # Definir fetcher baseado no modo escolhido
    if mode == "dinamico":
        fetcher = SeleniumConversationsFetcher(driver_path="chromedriver.exe", url="https://web.whatsapp.com/")  # TODO
    else:
        fetcher = LocalFileFetcher()

    # Gerar relatório diário
    report_generator = DailyReport(fetcher=fetcher, model_store="model_store.json")
    report = report_generator.generate_report()

    # Salvar relatório em JSON
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    print(f"📄 Relatório salvo em: {REPORT_PATH}")

    # Perguntar ao usuário se deseja ativar o feedback manual
    resposta = input("🔍 Deseja validar manualmente o relatório e fornecer feedback? (s/n): ").strip().lower()

    if resposta == "s":
        print("🔍 Modo de treinamento ativado! O relatório será analisado manualmente.")
        save_feedback_template()
        feedback_data = wait_for_feedback()

        # Aplicar feedback para aprendizado
        apply_feedback(feedback_data)
        print("✅ Feedback processado e aplicado ao modelo!")
    else:
        print("✅ Relatório finalizado sem feedback manual.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Workflow de Geração de Relatórios")
    parser.add_argument("mode", choices=["estatico", "dinamico"], help="Modo de execução do workflow")

    args = parser.parse_args()
    run_workflow(mode=args.mode)
