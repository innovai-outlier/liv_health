# src/reports/embedding_extractor.py

import os
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from .chat_parser import load_labeled_history
from .embedding_utils import EmbeddingsModel

class EmbeddingExtractor:
    """
    Faz multi-class: 'nao_agendou' -> 0, 'agendou' -> 1, 'cancelou' -> 2, 'pendencia' -> 3
    Necessita que a base histórica tenha esses rótulos.
    """
    def __init__(self, model_name="sentence-transformers/paraphrase-xlm-r-multilingual-v1"):
        self.emb_model = EmbeddingsModel(model_name)
        self.classifier = None
        # Quatro possíveis rótulos
        self.labels_map = {
            "nao_agendou": 0,
            "agendou": 1,
            "cancelou": 2,
            "pendencia": 3
        }
        # Mapa inverso para predict
        self.inv_labels_map = {v: k for k, v in self.labels_map.items()}

    def build_dataset(self, base_dir="assets/chatbase", max_samples_per_conv=2):
        """
        Lê conversas e gera (embedding, label).
        Supondo que 'label' no conv seja 'nao_agendou', 'agendou', 'cancelou', 'pendencia'
        Caso a base só tenha 'agendou' e 'nao_agendou', não terá dados p/ 'cancelou' e 'pendencia'.
        """
        conversas = load_labeled_history(base_dir=base_dir)
        X, y = [], []
        for conv in conversas:
            label_str = conv["label"]
            # Se não estiver no map, assume 'nao_agendou'
            label = self.labels_map.get(label_str, 0)
            msgs = conv["mensagens"]
            count = 0
            for msg in msgs[::-1]:
                if msg["from"] == "lead":
                    emb = self.emb_model.embed_sentence(msg["text"])
                    X.append(emb)
                    y.append(label)
                    count += 1
                if count >= max_samples_per_conv:
                    break
        return np.array(X), np.array(y)

    def train_classifier(self, X, y):
        """
        Treina logistic regression multi-class
        """
        self.classifier = LogisticRegression(multi_class='multinomial', solver='lbfgs')
        self.classifier.fit(X, y)
        score = self.classifier.score(X, y)
        print("Score no treinamento multi-class:", score)

    def save_classifier(self, path="model_store.json"):
        if self.classifier is None:
            return
        data = {
            "coef_": self.classifier.coef_.tolist(),
            "intercept_": self.classifier.intercept_.tolist()
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_classifier(self, path="model_store.json"):
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.classifier = LogisticRegression(multi_class='multinomial', solver='lbfgs')
        self.classifier.coef_ = np.array(data["coef_"])
        self.classifier.intercept_ = np.array(data["intercept_"])
        self.classifier.n_features_in_ = len(self.classifier.coef_[0])

    def predict_label(self, text):
        """
        Retorna uma das 4 classes: 'nao_agendou', 'agendou', 'cancelou', 'pendencia'
        """
        if self.classifier is None:
            return None
        emb = self.emb_model.embed_sentence(text)
        pred = self.classifier.predict([emb])[0]
        return self.inv_labels_map.get(pred, "nao_agendou")
