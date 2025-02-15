# sinonimos.py
import json
import nltk
from nltk.corpus import wordnet
from fuzzywuzzy import fuzz
from configuracoes import DICIONARIO_SINONIMOS, salvar_base_sinonimos

nltk.download("wordnet")

def encontrar_sinonimos(palavra):
    """Retorna uma lista de sinônimos para a palavra usando WordNet e a base dinâmica."""
    sinonimos = set(DICIONARIO_SINONIMOS.get(palavra, []))
    for synset in wordnet.synsets(palavra):
        for lemma in synset.lemmas():
            sinonimos.add(lemma.name().replace("_", " "))
    return sinonimos

def expandir_sinonimos(novas_palavras):
    """Adiciona novas palavras à base de sinônimos se forem similares a termos existentes."""
    for palavra in novas_palavras:
        for termo_base in DICIONARIO_SINONIMOS.keys():
            if fuzz.ratio(palavra, termo_base) > 80:
                if palavra not in DICIONARIO_SINONIMOS[termo_base]:
                    DICIONARIO_SINONIMOS[termo_base].append(palavra)
    salvar_base_sinonimos()
