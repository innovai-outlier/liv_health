# src/config/papis_config.py
import json
import os
from transformers import pipeline

# Arquivo JSON onde guardamos os chunks
ASSISTANT_PROMPT_JSON_FILE = "assets/assistente_prompt.json"

def load_prompt_chunks():
    """Carrega os chunks do arquivo JSON e retorna a lista de blocos."""
    if not os.path.exists(ASSISTANT_PROMPT_JSON_FILE):
        print(f"Arquivo não encontrado: {ASSISTANT_PROMPT_JSON_FILE}")
        return []
    with open(ASSISTANT_PROMPT_JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("assistant_prompt_chunks", [])

def carregar_modelos():
    """
    Retorna um dicionário com:
      - 'assistant_prompt_chunks': lista de chunks (cada chunk contém 'id' e 'content')
      - pipelines de geração para lead e assistente
      - parâmetros de geração, se necessário
    """
    prompt_chunks = load_prompt_chunks()

    # Pipelines locais
    lead_pipeline = pipeline("text-generation", model="EleutherAI/gpt-neo-125M", device=-1)
    assistente_pipeline = pipeline("text-generation", model="distilgpt2", device=-1)

    # Parâmetros de geração
    LEAD_GEN_PARAMS = {
        "max_new_tokens": 30,
        "do_sample": True,
        "temperature": 0.8,
        "pad_token_id": 50256,
    }
    ASSISTENTE_GEN_PARAMS = {
        "max_new_tokens": 30,
        "do_sample": True,
        "temperature": 0.6,
        "pad_token_id": 50256,
    }

    return {
        "assistant_prompt_chunks": prompt_chunks,
        "lead_model": lead_pipeline,
        "assistente_model": assistente_pipeline,
        "lead_params": LEAD_GEN_PARAMS,
        "assistente_params": ASSISTENTE_GEN_PARAMS,
    }
