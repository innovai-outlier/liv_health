# src/reports/embeddings_utils.py
from sentence_transformers import SentenceTransformer, util
import numpy as np

class EmbeddingsModel:
    def __init__(self, model_name="sentence-transformers/paraphrase-xlm-r-multilingual-v1"):
        self.model = SentenceTransformer(model_name)

    def embed_sentence(self, text):
        return self.model.encode(text, convert_to_numpy=True)

    def cosine_similarity(self, emb1, emb2):
        return float(util.cos_sim(emb1, emb2)[0][0])
