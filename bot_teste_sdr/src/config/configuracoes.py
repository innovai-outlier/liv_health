# configuracoes.py
import json
import nltk

nltk.download("wordnet")

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
