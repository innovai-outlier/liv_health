# src/analysis/analise.py
from src.config.constantes import (
    ALTA_APTIDAO_FUNIL, 
    BAIXA_APTIDAO_FUNIL,
    CONVERSAO_CONFIRMADA, 
    RESPOSTAS_GENERICAS, 
    RESPOSTAS_ROBOTICAS, 
    PROIBIDO_ENCAMINHAMENTO, 
    SERVICOS_DISPONIVEIS, 
    FUZZY_THRESHOLD
)
from src.analysis.sinonimos import encontrar_sinonimos
import re
from fuzzywuzzy import fuzz
import language_tool_python

language_tool = language_tool_python.LanguageTool("pt-BR")

def normalizar_texto(texto):
    texto = re.sub(r"^(Agente:\s*)", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"[^\w\s]", "", texto)
    return texto.lower().strip()

def contem_expressao_flexivel(texto, lista_expressao, threshold=FUZZY_THRESHOLD):
    texto_norm = normalizar_texto(texto)
    for expressao in lista_expressao:
        expressao_norm = normalizar_texto(expressao)
        if expressao_norm in texto_norm:
            return True
    for expressao in lista_expressao:
        expressao_norm = normalizar_texto(expressao)
        score = fuzz.token_set_ratio(texto_norm, expressao_norm)
        if score >= threshold:
            return True
    return False

def avaliar_aptidao_funil(conversa):
    alta = sum(1 for msg in conversa.split("\n") if contem_expressao_flexivel(msg, ALTA_APTIDAO_FUNIL))
    baixa = sum(1 for msg in conversa.split("\n") if contem_expressao_flexivel(msg, BAIXA_APTIDAO_FUNIL))
    return "Alta" if alta > baixa else "Baixa"

def avaliar_temperatura_lead(conversa, threshold=FUZZY_THRESHOLD):
    lead_msgs = [msg for msg in conversa.split("\n") if msg.startswith("Agente:")]
    if not lead_msgs:
        return 0
    first_msg = lead_msgs[0]
    from src.config.constantes import ALTA_TEMPERATURA, MEDIA_TEMPERATURA, BAIXA_TEMPERATURA
    if contem_expressao_flexivel(first_msg, ALTA_TEMPERATURA, threshold=threshold):
        return 10
    elif contem_expressao_flexivel(first_msg, MEDIA_TEMPERATURA, threshold=threshold):
        return 5
    elif contem_expressao_flexivel(first_msg, BAIXA_TEMPERATURA, threshold=threshold):
        return 2
    else:
        return 0

def avaliar_conversao(conversa):
    return "Convertido" if contem_expressao_flexivel(conversa, CONVERSAO_CONFIRMADA) else "Não Convertido"

def avaliar_respostas_genericas(conversa):
    respostas = [msg.split("SDR: ")[1] for msg in conversa.split("\n") if "SDR: " in msg]
    respostas_genericas = sum(1 for resposta in respostas if contem_expressao_flexivel(resposta, RESPOSTAS_GENERICAS))
    return round((respostas_genericas / len(respostas)) * 100, 2) if respostas else 0

def avaliar_grau_robotizacao(conversa):
    robotizacao = sum(1 for msg in conversa.split("\n") if contem_expressao_flexivel(msg, RESPOSTAS_ROBOTICAS))
    return min(robotizacao, 10)

def avaliar_compreensao_semantica(conversa):
    from fuzzywuzzy import fuzz
    perguntas = [msg.split("Agente: ")[1] for msg in conversa.split("\n") if "Agente: " in msg]
    respostas = [msg.split("SDR: ")[1] for msg in conversa.split("\n") if "SDR: " in msg]
    pares = list(zip(perguntas, respostas))
    if not pares:
        return 1.0
    total_score = sum(fuzz.token_set_ratio(q, a)/100.0 for q, a in pares)
    media = total_score / len(pares)
    return round(media, 2)

def avaliar_adequacao_gramatical(conversa):
    respostas = [msg.split("SDR: ")[1] for msg in conversa.split("\n") if "SDR: " in msg]
    erros_totais = sum(len(language_tool.check(resposta)) for resposta in respostas)
    return round(1 - (erros_totais / (len(respostas) * 5)), 2) if respostas else 1.0

def avaliar_respeito_encaminhamento(conversa):
    erros = sum(1 for msg in conversa.split("\n") if contem_expressao_flexivel(msg, PROIBIDO_ENCAMINHAMENTO))
    return round(1 - (erros / 10), 2) if erros < 10 else 0

def avaliar_conhecimento_servicos(conversa):
    mencoes = sum(1 for msg in conversa.split("\n") if contem_expressao_flexivel(msg, SERVICOS_DISPONIVEIS))
    return round(mencoes / 5, 2) if mencoes > 0 else 0
