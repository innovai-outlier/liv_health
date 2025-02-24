# src/reports/daily_report.py
import re
from datetime import datetime

from .fetcher_base import ConversationsFetcher
from .keyword_utils import load_keywords_db

class DailyReport:
    """
    Gera relatório diário de conversas, com métricas:
    - agendamentos_realizados
    - cancelamentos_consultas
    - pendencias_ao_medico
    """

    def __init__(self, fetcher: ConversationsFetcher, keywords_file="keywords_db.json"):
        self.fetcher = fetcher
        self.keywords_db = load_keywords_db(keywords_file)

    def generate_report(self):
        conversas = self.fetcher.fetch_today_conversations()
        data_hoje = datetime.now().strftime("%Y-%m-%d")

        agendamentos = 0
        cancelamentos = 0
        pendencias = 0

        detalhes_conversas = []

        for conv in conversas:
            lead_id = conv.get("lead_id", "desconhecido")
            msgs = conv.get("mensagens", [])

            # Juntar todo texto em lowercase
            texto_completo = "\n".join(msg["text"].lower() for msg in msgs)

            # Pegar as listas de keywords
            agend_list = self.keywords_db.get("agendamentos", [])
            cancel_list = self.keywords_db.get("cancelamentos", [])
            pend_list = self.keywords_db.get("pendencias_medico", [])

            c_agend = self._count_keywords(texto_completo, agend_list)
            c_cancel = self._count_keywords(texto_completo, cancel_list)
            c_pend = self._count_keywords(texto_completo, pend_list)

            if c_agend > 0:
                agendamentos += 1
            if c_cancel > 0:
                cancelamentos += 1
            pendencias += c_pend

            detalhes_conversas.append({
                "lead_id": lead_id,
                "num_msgs": len(msgs),
                "agendamentos_detectados": c_agend,
                "cancelamentos_detectados": c_cancel,
                "pendencias_detectadas": c_pend
            })

        relatorio = {
            "data": data_hoje,
            "total_conversas_hoje": len(conversas),
            "agendamentos_realizados": agendamentos,
            "cancelamentos_consultas": cancelamentos,
            "pendencias_ao_medico": pendencias,
            "detalhes": detalhes_conversas
        }
        return relatorio

    def _count_keywords(self, text, keywords_list):
        count = 0
        for kw in keywords_list:
            pattern = re.escape(kw.lower())
            matches = re.findall(pattern, text)
            count += len(matches)
        return count
