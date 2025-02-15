# analise.py
from configuracoes import DICIONARIO_SINONIMOS
from constantes import (
    ALTA_APTIDAO_FUNIL, BAIXA_APTIDAO_FUNIL, ALTA_TEMPERATURA, MEDIA_TEMPERATURA, BAIXA_TEMPERATURA,
    CONVERSAO_CONFIRMADA, RESPOSTAS_GENERICAS, RESPOSTAS_ROBOTICAS, PROIBIDO_ENCAMINHAMENTO, SERVICOS_DISPONIVEIS
)
from sinonimos import encontrar_sinonimos
import re
from fuzzywuzzy import fuzz
import language_tool_python

# Inicializa o corretor gramatical
language_tool = language_tool_python.LanguageTool("pt-BR")

def contem_expressao(texto, lista_expressao):
    """Verifica se o texto contém alguma expressão (ou seus sinônimos) da lista."""
    for expressao in lista_expressao:
        sinonimos = encontrar_sinonimos(expressao)
        sinonimos.add(expressao)
        for termo in sinonimos:
            if re.search(rf"\b{termo}\b", texto, re.IGNORECASE):
                return True
    return False

def avaliar_aptidao_funil(conversa):
    """Avalia se o lead tem alta ou baixa aptidão para o funil."""
    alta = sum(1 for msg in conversa.split("\n") if contem_expressao(msg, ALTA_APTIDAO_FUNIL))
    baixa = sum(1 for msg in conversa.split("\n") if contem_expressao(msg, BAIXA_APTIDAO_FUNIL))
    return "Alta" if alta > baixa else "Baixa"

def avaliar_temperatura_lead(conversa):
    """Determina a temperatura do lead (escala 1-10)."""
    score = 0
    for msg in conversa.split("\n"):
        if contem_expressao(msg, ALTA_TEMPERATURA):
            score += 3
        elif contem_expressao(msg, MEDIA_TEMPERATURA):
            score += 2
        elif contem_expressao(msg, BAIXA_TEMPERATURA):
            score += 1
    return min(score, 10)

def avaliar_conversao(conversa):
    """Verifica se há sinais de conversão no contexto."""
    return "Convertido" if contem_expressao(conversa, CONVERSAO_CONFIRMADA) else "Não Convertido"

def avaliar_respostas_genericas(conversa):
    """Calcula a porcentagem de respostas genéricas da assistente."""
    respostas = [msg.split("SDR: ")[1] for msg in conversa.split("\n") if "SDR: " in msg]
    respostas_genericas = sum(1 for resposta in respostas if contem_expressao(resposta, RESPOSTAS_GENERICAS))
    return round((respostas_genericas / len(respostas)) * 100, 2) if respostas else 0

def avaliar_grau_robotizacao(conversa):
    """Determina o grau de robotização (0-10) da assistente."""
    robotizacao = sum(1 for msg in conversa.split("\n") if contem_expressao(msg, RESPOSTAS_ROBOTICAS))
    return min(robotizacao, 10)

def avaliar_compreensao_semantica(conversa):
    """Avalia se a assistente mantém o contexto da conversa."""
    perguntas = [msg.split("Agente: ")[1] for msg in conversa.split("\n") if "Agente: " in msg]
    respostas = [msg.split("SDR: ")[1] for msg in conversa.split("\n") if "SDR: " in msg]
    erros = sum(1 for i in range(len(perguntas)-1) if perguntas[i] not in respostas[i+1])
    return round(1 - (erros / len(perguntas)), 2) if perguntas else 1.0

def avaliar_adequacao_gramatical(conversa):
    """Avalia a correção gramatical das respostas da assistente."""
    respostas = [msg.split("SDR: ")[1] for msg in conversa.split("\n") if "SDR: " in msg]
    erros_totais = sum(len(language_tool.check(resposta)) for resposta in respostas)
    return round(1 - (erros_totais / (len(respostas) * 5)), 2) if respostas else 1.0

def avaliar_respeito_encaminhamento(conversa):
    """Verifica se a assistente não sugeriu tratamentos."""
    erros = sum(1 for msg in conversa.split("\n") if contem_expressao(msg, PROIBIDO_ENCAMINHAMENTO))
    return round(1 - (erros / 10), 2) if erros < 10 else 0

def avaliar_conhecimento_servicos(conversa):
    """Verifica se a assistente mencionou corretamente os serviços disponíveis."""
    mencoes = sum(1 for msg in conversa.split("\n") if contem_expressao(msg, SERVICOS_DISPONIVEIS))
    return round(mencoes / 5, 2) if mencoes > 0 else 0
