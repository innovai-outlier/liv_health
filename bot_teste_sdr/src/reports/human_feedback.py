import json
import os
import time

FEEDBACK_FILE = "output/feedback.json"
RELATORIO_FILE = "output/relatorio_diario.json"

def gerar_template_feedback():
    """Cria um arquivo de feedback.json vazio para preenchimento manual."""
    if not os.path.exists(RELATORIO_FILE):
        print("❌ Relatório diário não encontrado! Gere o relatório antes de validar o feedback.")
        return

    with open(RELATORIO_FILE, "r", encoding="utf-8") as f:
        relatorio = json.load(f)

    feedback_template = {
        "data": relatorio.get("data"),
        "avaliador": "",
        "comentarios_gerais": "",
        "correcoes_metricas": []
    }

    for item in relatorio["detalhes"]:
        feedback_template["correcoes_metricas"].append({
            "lead_id": item["lead_id"],
            "agendamentos_detectados": item["agendamentos_detectados"],
            "correcao_agendamentos": item["agendamentos_detectados"],
            "cancelamentos_detectados": item["cancelamentos_detectados"],
            "correcao_cancelamentos": item["cancelamentos_detectados"],
            "pendencias_detectadas": item["pendencias_detectadas"],
            "correcao_pendencias": item["pendencias_detectadas"],
            "observacoes": ""
        })

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback_template, f, indent=4, ensure_ascii=False)

    print(f"✅ Arquivo de feedback gerado: {FEEDBACK_FILE}")
    print("✍️  Agora edite manualmente esse arquivo e preencha os campos necessários.")

def aguardar_feedback():
    """Aguarda até que o feedback seja preenchido manualmente."""
    print("\n🔄 Aguardando preenchimento do feedback... Digite 's' quando estiver pronto para continuar.")
    
    while True:
        resposta = input("O feedback foi preenchido? (s/n): ").strip().lower()
        if resposta == "s":
            break
        print("⏳ Aguardando... Por favor, preencha o arquivo antes de continuar.")

def aplicar_feedback():
    """Carrega e aplica o feedback preenchido ao sistema."""
    if not os.path.exists(FEEDBACK_FILE):
        print("❌ Arquivo de feedback não encontrado. Gere o feedback primeiro.")
        return

    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        feedback = json.load(f)

    print("\n📊 Aplicando feedback ao relatório...")
    
    for correcao in feedback["correcoes_metricas"]:
        print(f"\n🎯 Lead ID: {correcao['lead_id']}")
        print(f"🔹 Agendamentos: {correcao['agendamentos_detectados']} → {correcao['correcao_agendamentos']}")
        print(f"❌ Cancelamentos: {correcao['cancelamentos_detectados']} → {correcao['correcao_cancelamentos']}")
        print(f"⚠️ Pendências: {correcao['pendencias_detectadas']} → {correcao['correcao_pendencias']}")
        print(f"📝 Observação: {correcao['observacoes']}")

    print("\n✅ Feedback processado com sucesso! As correções podem agora ser incorporadas ao modelo.")

if __name__ == "__main__":
    gerar_template_feedback()
    aguardar_feedback()
    aplicar_feedback()
