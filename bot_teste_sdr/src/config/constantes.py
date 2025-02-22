# constantes.py

# Expressões para leads com alta aptidão no funil
ALTA_APTIDAO_FUNIL = [
    "quero agendar", "vou agendar", "preciso marcar", "marcar consulta",
    "agendar consulta", "quero marcar", "marcar minha consulta"
]

# Expressões para leads com baixa aptidão no funil
BAIXA_APTIDAO_FUNIL = [
    "preço", "desconto", "parcelamento", "vou pensar", "tem promoção",
    "dúvidas sobre preço", "valor elevado"
]

# Indicadores de temperatura do lead
ALTA_TEMPERATURA = [
    "quero agendar", "estou pronto", "pode marcar", "agendar imediatamente"
]
MEDIA_TEMPERATURA = [
    "quero saber mais", "como funciona", "pode me explicar melhor", "diga mais sobre"
]
BAIXA_TEMPERATURA = [
    "só estou pesquisando", "vou pensar", "não tenho certeza", "apenas olhando"
]

# Frases que indicam conversão
CONVERSAO_CONFIRMADA = [
    "vou agendar", "pode marcar", "quero confirmar meu horário"
]

# Frases que indicam respostas genéricas da assistente
RESPOSTAS_GENERICAS = [
    "não sei", "vou verificar", "posso ajudar", "me fale mais", "essa informação não está disponível"
]

# Frases que indicam alta robotização
RESPOSTAS_ROBOTICAS = [
    "de acordo com", "nosso sistema indica", "essa é a resposta padrão", "nosso protocolo"
]

# Expressões proibidas (a assistente não deve recomendar tratamentos)
PROIBIDO_ENCAMINHAMENTO = [
    "remédio", "tratamento", "tome", "use", "melhorar", "diagnóstico", "evitar"
]

# Palavras que indicam conhecimento dos serviços oferecidos
SERVICOS_DISPONIVEIS = [
    "exames", "procedimentos", "planos", "consulta médica", "tratamento disponível"
]

# Parâmetro para fuzzy matching
FUZZY_THRESHOLD = 70
