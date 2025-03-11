import os
import json
import argparse
#from src.reports.daily_report import DailyReport
from src.reports.generative_model import GenerativeReportGenerator
from src.reports.fetcher_base import LocalFileFetcher
from src.reports.apply_feedback import aplicar_feedback
from src.reports.embedding_extractor import EmbeddingExtractor

# Caminhos dos arquivos de saída
OUTPUT_DIR = "output"
MODEL_PATH = os.path.join(OUTPUT_DIR, "model_store.json")
REPORT_EMBEDDINGS = os.path.join(OUTPUT_DIR, "daily_report.json")
REPORT_GENERATIVE = os.path.join(OUTPUT_DIR, "generative_daily_report.json")
FEEDBACK_FILE = os.path.join(OUTPUT_DIR, "feedback.json")

# Garante que o diretório de saída existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

def train_model():
    """ Treina o modelo de embeddings usando `database/train/` """
    print("🚀 Treinando modelo com base `train/`...")
    
    extractor = EmbeddingExtractor()
    X, y = extractor.build_dataset(base_type="train")

    if len(set(y)) < 2:
        print("⚠️ ERRO: Apenas uma classe detectada. O treinamento requer pelo menos duas classes diferentes.")
        return

    extractor.train_classifier(X, y)
    extractor.save_classifier()
    print(f"✅ Modelo treinado e salvo em {extractor.model_store}")

def generate_report(base_type="test", use_generative=True, target_date=None, assistente=None, showtime=False):
    """ Gera relatórios usando embeddings ou IA Generativa na base correta """
    print(f"📊 Gerando relatório para `{base_type}`...")

    #fetcher = LocalFileFetcher(base_type=base_type)
    fetcher = LocalFileFetcher(base_type=base_type)  # Usuário escolhe um diretório com JSONs
    conversas = fetcher.fetch_today_conversations(target_date=target_date)
    print()
    if showtime:
        output_path = "output/GPT_EXPECTED_OUTPUT.json"
        print(f"✅ Relatório salvo em {output_path}")
        return

    if use_generative:
        print("🤖 Usando IA Generativa para gerar relatório...")
        grg = GenerativeReportGenerator()
        #conversas = model.load_conversations(target_date=target_date)
        report = grg.generate_report(conversas)
    else:
        print("🔎 Usando modelo de embeddings...")
        extractor = EmbeddingExtractor()
        report_generator = DailyReport(fetcher=fetcher, model_store=extractor.model_store)
        report = report_generator.generate_report()
    if (assistente == None):
        output_path = f"output/{base_type}_report.json"
    else:
        output_path = f"output/{assistente}_{target_date}_report.json"
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f"✅ Relatório salvo em {output_path}")
    
def request_feedback():
    """ Pergunta ao usuário se deseja fornecer feedback e espera a validação manual """
    print("\n⚠️ Aguardando validação humana...")
    print("Abra o arquivo abaixo e preencha com os ajustes necessários:")
    print(f"📂 {FEEDBACK_FILE}")

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump({"status": "pending", "comentarios": ""}, f, indent=4, ensure_ascii=False)

    while True:
        input("\n🔍 Pressione ENTER para verificar se o feedback foi preenchido...")
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                feedback_data = json.load(f)
            if feedback_data.get("status") == "complete":
                print("✅ Feedback confirmado! Aplicando ajustes...")
                return feedback_data
            else:
                print("⚠️ Feedback ainda não preenchido. Aguarde e tente novamente.")
        except Exception as e:
            print(f"❌ Erro ao ler o feedback: {e}")

def apply_feedback():
    """ Aplica o feedback ao modelo para refinamento """
    if not os.path.exists(FEEDBACK_FILE):
        print("⚠️ Nenhum feedback encontrado. Execute a validação primeiro.")
        return

    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        feedback_data = json.load(f)

    apply_feedback_to_model(feedback_data)
    print("✅ Feedback aplicado ao modelo com sucesso!")

def main():
    parser = argparse.ArgumentParser(description="Executa workflow de geração de relatórios")
    parser.add_argument("mode", choices=["train", "test", "validate", "use_generative", "apply_feedback"],
                        help="Escolha o modo de execução")
    parser.add_argument("--feedback", action="store_true",
                        help="Solicitar feedback humano antes de concluir")
    
    args = parser.parse_args()

    if args.mode == "train":
        train_model()
    elif args.mode in ["test", "validate"]:
        generate_report(args.mode)
        if args.feedback:
            feedback_data = request_feedback()
            if feedback_data:
                apply_feedback()
    elif args.mode == "use_generative":
        generate_report("test", use_generative=True)
    elif args.mode == "apply_feedback":
        apply_feedback()
    else:
        print("❌ Opção inválida. Use --help para mais informações.")

if __name__ == "__main__":
    main()
