import json
import os
from src.reports.embedding_extractor import EmbeddingExtractor
from src.reports.keyword_utils import load_keywords, save_keywords

FEEDBACK_FILE = "output/feedback.json"
KEYWORDS_DB = "src/reports/keywords_db.json"
MODEL_STORE = "src/reports/model_store.json"

def aplicar_feedback():
    """Incorpora feedback humano ao modelo e atualiza a base de aprendizado"""
    if not os.path.exists(FEEDBACK_FILE):
        print("❌ Nenhum feedback encontrado. Preencha `feedback.json` primeiro.")
        return

    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        feedback = json.load(f)

    print("\n📊 Aplicando feedback...")

    # 1️⃣ Atualizar palavras-chave e sinônimos
    keywords = load_keywords(KEYWORDS_DB)

    for correcao in feedback["correcoes_metricas"]:
        lead_id = correcao["lead_id"]
        if correcao["correcao_agendamentos"] > correcao["agendamentos_detectados"]:
            keywords["agendou"].append(f"Correção de {lead_id}")
        if correcao["correcao_cancelamentos"] > correcao["cancelamentos_detectados"]:
            keywords["cancelou"].append(f"Correção de {lead_id}")
        if correcao["correcao_pendencias"] > correcao["pendencias_detectadas"]:
            keywords["pendencia"].append(f"Correção de {lead_id}")

    save_keywords(KEYWORDS_DB, keywords)

    # 2️⃣ Atualizar modelo de embeddings
    print("\n🔄 Re-treinando o modelo com dados corrigidos...")
    extractor = EmbeddingExtractor()
    X, y = extractor.build_dataset(base_dir="assets/chatbase")
    extractor.train_classifier(X, y)
    extractor.save_classifier(MODEL_STORE)

    print("\n✅ Feedback aplicado! Modelo atualizado com aprendizado contínuo.")

if __name__ == "__main__":
    aplicar_feedback()
