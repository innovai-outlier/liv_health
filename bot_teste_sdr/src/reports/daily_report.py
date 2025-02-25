# src/reports/daily_report.py
import os
from datetime import datetime

from .fetcher_base import ConversationsFetcher
from .embedding_extractor import EmbeddingExtractor

class DailyReport:
    def __init__(self, fetcher: ConversationsFetcher, model_store="model_store.json"):
        self.fetcher = fetcher
        self.extractor = EmbeddingExtractor()  # multi-class
        self.extractor.load_classifier(model_store)
        # Expressões que indicam pendência resolvida
        self.resolve_keywords = ["resolvido", "enviado", "emitido", "providenciei", "nota emitida"]

    def generate_report(self):
        conversas = self.fetcher.fetch_today_conversations()
        data_hoje = datetime.now().strftime("%Y-%m-%d")

        # contadores
        total_conversas = len(conversas)
        agendamentos = 0
        cancelamentos = 0
        pendencias = 0

        detalhes = []

        for conv in conversas:
            lead_id = conv.get("lead_id", "desconhecido")
            msgs = conv.get("mensagens", [])

            # Faremos uma varredura
            # is_agendou => se encontrar msgs 'agendou'
            # is_cancelou => se encontrar 'cancelou'
            # is_pendencia => se encontrar 'pendencia' sem 'resolvido'
            # default => 'nao_agendou'
            # Pode haver multiplas msgs, pegamos a "classe" predominante?

            # Exemplo: contagem
            label_count = {
                "nao_agendou": 0,
                "agendou": 0,
                "cancelou": 0,
                "pendencia": 0
            }

            # Para ver se algo foi resolvido
            pendencias_detectadas = 0  # conta quantas msgs do lead foram 'pendencia'
            pendencias_resolvidas = 0

            for i, msg in enumerate(msgs):
                text_low = msg["text"].lower()
                # Prever a classe
                predicted_label = self.extractor.predict_label(msg["text"]) if msg["from"] == "lead" else "nao_agendou"

                if predicted_label in label_count:
                    label_count[predicted_label] += 1

                # Caso predicted_label='pendencia'
                if predicted_label == "pendencia":
                    pendencias_detectadas += 1

                # Checar se o assistente fala algo "resolvido," etc.
                if msg["from"] == "assistente":
                    if any(k in text_low for k in self.resolve_keywords):
                        # Consideramos que 1 pendencia resolvida
                        # Em logica real, poderia vincular ao idx anterior do lead
                        if pendencias_detectadas > pendencias_resolvidas:
                            pendencias_resolvidas += 1

            # Decide label final
            # Exemplo: pega o maior count
            final_label = max(label_count, key=label_count.get)

            # se final_label='agendou' => agendamentos++
            # se final_label='cancelou' => cancelamentos++
            # se final_label='pendencia' => pendencias++ (mas se resolvida < detectada)
            if final_label == "agendou":
                agendamentos += 1
            elif final_label == "cancelou":
                cancelamentos += 1

            # Pendencias => se pendencias_detectadas>pendencias_resolvidas => real pendencia
            has_pendencia = (pendencias_detectadas > pendencias_resolvidas)
            if has_pendencia:
                pendencias += 1

            detalhes.append({
                "lead_id": lead_id,
                "label_count": label_count,
                "pendencias_detectadas": pendencias_detectadas,
                "pendencias_resolvidas": pendencias_resolvidas,
                "final_label": final_label,
                "has_pendencia": has_pendencia
            })

        relatorio = {
            "data": data_hoje,
            "total_conversas": total_conversas,
            "agendamentos_realizados": agendamentos,
            "cancelamentos_consultas": cancelamentos,
            "pendencias_ao_medico": pendencias,
            "detalhes": detalhes
        }
        return relatorio
