# configuracoes.py
import json
import nltk
from transformers import pipeline

nltk.download("wordnet")

# Carregar a base de sinônimos de um arquivo ou criar uma nova
try:
    with open("sinonimos.json", "r", encoding="utf-8") as f:
        DICIONARIO_SINONIMOS = json.load(f)
except FileNotFoundError:
    DICIONARIO_SINONIMOS = {
        "agendar": ["marcar", "reservar", "confirmar", "fazer um agendamento"],
        "consulta": ["atendimento", "exame médico", "avaliação"],
        "interesse": ["curiosidade", "desejo", "vontade"],
        "preço": ["custo", "valor", "investimento"],
        "desconto": ["promoção", "redução", "oferta especial"],
    }

def salvar_base_sinonimos():
    """Salva a base de sinônimos atualizada."""
    with open("sinonimos.json", "w", encoding="utf-8") as f:
        json.dump(DICIONARIO_SINONIMOS, f, indent=4, ensure_ascii=False)

def carregar_modelos():
    """Carrega modelos de IA para geração de mensagens para agentes."""
    return {
        "critico": pipeline("text-generation", model="mistralai/Mistral-7B-v0.1"),
        "moderado": pipeline("text-generation", model="mistralai/Mistral-7B-v0.1"),
        "desinformado": pipeline("text-generation", model="mistralai/Mistral-7B-v0.1"),
        "indeciso": pipeline("text-generation", model="mistralai/Mistral-7B-v0.1"),
        "questionador": pipeline("text-generation", model="mistralai/Mistral-7B-v0.1"),
        "spam": pipeline("text-generation", model="mistralai/Mistral-7B-v0.1")
    }
