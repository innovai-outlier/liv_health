# main.py
import argparse
import time
import pandas as pd
from configuracoes import carregar_modelos
from agentes import Lead, Assistente
from selenium_bot import iniciar_selenium, enviar_mensagem, capturar_resposta
from analise import (avaliar_aptidao_funil, avaliar_temperatura_lead, avaliar_conversao,
                     avaliar_respostas_genericas, avaliar_grau_robotizacao, avaliar_compreensao_semantica,
                     avaliar_adequacao_gramatical, avaliar_respeito_encaminhamento, avaliar_conhecimento_servicos)
from base_conversas import adicionar_conversa, buscar_conversa_similar, carregar_conversas
from sinonimos import expandir_sinonimos

# Configuração de argumentos para auditoria
parser = argparse.ArgumentParser(description="Auditoria da Assistente Virtual")
parser.add_argument("--tipo", choices=["dinamica", "estatica"], required=True,
                    help="Tipo de auditoria: dinamica ou estatica")
args = parser.parse_args()

if args.tipo == "dinamica":
    modelos = carregar_modelos()
    driver = iniciar_selenium()

# Lista para armazenar novas palavras encontradas durante a auditoria
novas_palavras = set()
resultados_teste = {}

# Para auditoria dinâmica, usamos perfis pré-definidos para leads
lead_profiles = ["critico", "moderado", "desinformado", "indeciso", "questionador", "spam"]

# Para auditoria estática, a lista de leads é derivada da base de conversas (aqui exemplificada)
if args.tipo == "estatica":
    base = carregar_conversas()
    # Exemplo: obter IDs ou nomes únicos de leads da base histórica
    leads_estaticos = [conv["id"] for conv in base["conversas"]]
else:
    leads_estaticos = lead_profiles

for lead_name in leads_estaticos:
    print(f"\n🔹 Iniciando auditoria para o lead: {lead_name}")
    
    # Cria objeto Lead
    if args.tipo == "dinamica":
        lead = Lead(name=lead_name, profile=lead_name, mode="dinamico")
    else:
        lead = Lead(name=lead_name, profile=lead_name, mode="estatico")
        conversa_existente = buscar_conversa_similar("exemplo de mensagem")
        if conversa_existente:
            print(f"Conversa estática encontrada para {lead_name} (ID {conversa_existente['id']})")
            for troca in conversa_existente["mensagens"]:
                lead.add_message("lead", troca.get("agente", ""))
                lead.add_message("assistente", troca.get("assistente", ""))
            resultados_teste[lead_name] = conversa_existente["metricas"]
            continue

    if args.tipo == "dinamica":
        for i in range(10):
            mensagem = f"Mensagem do {lead.profile} - turno {i+1}"
            lead.add_message("lead", mensagem)
            enviar_mensagem(driver, mensagem)
            inicio = time.time()
            resposta = capturar_resposta(driver)
            fim = time.time()
            if resposta:
                lead.add_message("assistente", resposta)
                tempo_resposta = round(fim - inicio, 2)
                novas_palavras.update(resposta.lower().split())
            else:
                print("Nenhuma resposta recebida. Encerrando auditoria para este lead.")
                break

    conversa_texto = lead.get_conversation()
    aptidao_funil = avaliar_aptidao_funil(conversa_texto)
    temperatura_lead = avaliar_temperatura_lead(conversa_texto)
    conversao = avaliar_conversao(conversa_texto)
    respostas_genericas = avaliar_respostas_genericas(conversa_texto)
    grau_robotizacao = avaliar_grau_robotizacao(conversa_texto)
    compreensao_semantica = avaliar_compreensao_semantica(conversa_texto)
    adequacao_gramatical = avaliar_adequacao_gramatical(conversa_texto)
    respeito_encaminhamento = avaliar_respeito_encaminhamento(conversa_texto)
    conhecimento_servicos = avaliar_conhecimento_servicos(conversa_texto)

    metricas = {
        "Aptidão para o Funil": aptidao_funil,
        "Temperatura do Lead": temperatura_lead,
        "Conversão": conversao,
        "Respostas Genéricas (%)": respostas_genericas,
        "Grau de Robotização": grau_robotizacao,
        "Compreensão Semântica": compreensao_semantica,
        "Adequação Gramatical": adequacao_gramatical,
        "Respeito à Regra de Encaminhamento": respeito_encaminhamento,
        "Conhecimento dos Serviços": conhecimento_servicos
    }

    resultados_teste[lead.name] = metricas

    if args.tipo == "dinamica":
        conversas = []
        # Organiza as mensagens para salvar na base
        msgs = lead.messages
        for idx in range(0, len(msgs), 2):
            conversa_item = {"agente": msgs[idx]["content"]}
            if idx + 1 < len(msgs):
                conversa_item["assistente"] = msgs[idx+1]["content"]
            conversas.append(conversa_item)
        adicionar_conversa("dinamica", conversas, metricas)

# Expande a base de sinônimos com novas palavras detectadas
expandir_sinonimos(novas_palavras)

df_resultados = pd.DataFrame(resultados_teste).T.reset_index().rename(columns={"index": "Lead"})
print("\nResultados da Auditoria:")
print(df_resultados)
