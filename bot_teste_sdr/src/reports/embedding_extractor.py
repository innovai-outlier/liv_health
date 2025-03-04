import os
import json
import numpy as np
from src.reports.chat_parser import load_labeled_history
from src.reports.embedding_utils import EmbeddingsModel

class EmbeddingExtractor:
    """
    Classe para treinar e usar um classificador de embeddings.
    Pode lidar com múltiplas classes: 'agendou', 'nao_agendou', 'cancelou', 'pendencia'.
    """

    def __init__(self, model_store="output/model_store.json"):
        self.model_store = model_store
        self.emb_model = EmbeddingsModel()  # Modelo de embeddings
        self.classifier = None
        self.labels_map = {"nao_agendou": 0, "agendou": 1, "cancelou": 2, "pendencia": 3}
        self.inv_labels_map = {v: k for k, v in self.labels_map.items()}

    def build_dataset(self, base_type="train", max_samples_per_conv=2):
        """
        Lê conversas e gera (embedding, label) baseado na base escolhida.
        - `base_type`: "train", "test" ou "validate"
        - `max_samples_per_conv`: Máximo de mensagens de um lead por conversa a serem usadas.
        """
        base_dir = f"database/{base_type}"
        file_path = os.path.join(base_dir, "conversations.json")

        if not os.path.exists(file_path):
            print(f"⚠️ ERRO: Base {base_type} não encontrada ({file_path})")
            return np.array([]), np.array([])

        # Carrega as conversas da base correta (train/test/validate)
        with open(file_path, "r", encoding="utf-8") as f:
            conversas = json.load(f)

        X, y = [], []
        for conv in conversas:
            label_str = conv["label"]
            label = self.labels_map.get(label_str, 0)  # Se não encontrado, assume 'nao_agendou'
            
            msgs = conv["mensagens"]
            count = 0
            for msg in msgs[::-1]:  # Processa mensagens do fim para o início
                if msg["from"] == "lead":
                    emb = self.emb_model.embed_sentence(msg["text"])
                    X.append(emb)
                    y.append(label)
                    count += 1
                if count >= max_samples_per_conv:
                    break

        print(f"✅ Dataset carregado de {base_type}: {len(X)} amostras")
        return np.array(X), np.array(y)

    def train_classifier(self, X, y):
        """ Treina um classificador de embeddings (Logistic Regression). """
        from sklearn.linear_model import LogisticRegression
        self.classifier = LogisticRegression(max_iter=1000)
        self.classifier.fit(X, y)
        print("✅ Modelo treinado com sucesso!")

    def save_classifier(self):
        """ Salva o modelo treinado corretamente, incluindo `classes_`. """
        if self.classifier is None:
            print("⚠️ Nenhum modelo treinado para salvar.")
            return

        model_data = {
            "coef_": self.classifier.coef_.tolist(),
            "intercept_": self.classifier.intercept_.tolist(),
            "classes_": self.classifier.classes_.tolist()  # Salvar classes corretamente
        }

        with open(self.model_store, "w", encoding="utf-8") as f:
            json.dump(model_data, f, indent=4, ensure_ascii=False)

        print(f"✅ Modelo salvo em {self.model_store}")

    def load_classifier(self):
        """ Carrega um modelo salvo corretamente. """
        if not os.path.exists(self.model_store):
            print("⚠️ Nenhum modelo encontrado. Treine primeiro.")
            return

        from sklearn.linear_model import LogisticRegression

        with open(self.model_store, "r", encoding="utf-8") as f:
            model_data = json.load(f)

        self.classifier = LogisticRegression(max_iter=1000)
        self.classifier.coef_ = np.array(model_data["coef_"])
        self.classifier.intercept_ = np.array(model_data["intercept_"])
        self.classifier.classes_ = np.array(model_data["classes_"])  # Restaurando as classes corretamente

        print("✅ Modelo carregado com sucesso!")


    def predict_label(self, text):
        """
        Retorna uma das classes: 'nao_agendou', 'agendou', 'cancelou', 'pendencia'.
        """
        if self.classifier is None:
            print("⚠️ Modelo não carregado!")
            return "nao_agendou"

        emb = self.emb_model.embed_sentence(text)
        pred = self.classifier.predict([emb])[0]

        #print(f"🧐 DEBUG: Texto: {text}\n   → Predição: {pred}")

        return self.inv_labels_map.get(pred, "nao_agendou")


# Teste rápido (comente se não estiver testando diretamente)
if __name__ == "__main__":
    extractor = EmbeddingExtractor()
    X_train, y_train = extractor.build_dataset("train")

    if len(X_train) > 0:
        extractor.train_classifier(X_train, y_train)
        extractor.save_classifier()
