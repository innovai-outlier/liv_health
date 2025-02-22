# src/storage/base_conversas.py
import json
from fuzzywuzzy import fuzz

CONVERSAS_JSON = "conversas.json"

def carregar_conversas():
    try:
        with open(CONVERSAS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"conversas": []}

def salvar_conversas(base):
    with open(CONVERSAS_JSON, "w", encoding="utf-8") as f:
        json.dump(base, f, indent=4, ensure_ascii=False)

def adicionar_conversa(tipo, mensagens, metricas):
    base = carregar_conversas()
    nova_conversa = {
        "id": f"conv_{len(base['conversas']) + 1:03}",
        "tipo": tipo,
        "mensagens": mensagens,
        "metricas": metricas
    }
    base["conversas"].append(nova_conversa)
    salvar_conversas(base)

def buscar_conversa_similar(mensagem):
    base = carregar_conversas()
    melhor_match = None
    maior_similaridade = 0
    for conv in base["conversas"]:
        for troca in conv["mensagens"]:
            similaridade = fuzz.token_sort_ratio(mensagem, troca.get("agente", ""))
            if similaridade > maior_similaridade:
                maior_similaridade = similaridade
                melhor_match = conv
    return melhor_match if maior_similaridade > 80 else None
