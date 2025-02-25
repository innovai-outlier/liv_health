# tests/reports/real_data_tests/test_real_daily_report.py
import unittest
import os
from src.reports.daily_report import DailyReport
from src.reports.fetcher_base import ConversationsFetcher
from src.reports.keyword_utils import load_keywords_db, save_keywords_db
from src.reports.chat_parser import load_labeled_history

class LocalFileFetcher(ConversationsFetcher):
    """
    Exemplo: mocka 'fetch_today_conversations' lendo
    assets/chatbase e transformando as conversas em
    dicionário no formato do daily_report.
    """

    def fetch_today_conversations(self):
        # Carrega success/fail e unifica
        conversas = load_labeled_history(base_dir="assets/chatbase")
        # Precisamos transformar cada item do load_labeled_history
        # em algo que daily_report espera:
        # [
        #   {
        #     "lead_id": "n/a",
        #     "mensagens": [ { "from": "lead"/"assistente", "text": "...", "timestamp": "..." }, ... ],
        #     "timestamp": "..."
        #   }
        # ]
        # Podemos só usar label p/ lead_id
        final_list = []
        for conv in conversas:
            final_list.append({
                "lead_id": conv["label"],
                "mensagens": conv["mensagens"],
                "timestamp": conv["mensagens"][0]["timestamp"] if conv["mensagens"] else "N/A"
            })
        return final_list

class TestRealDailyReport(unittest.TestCase):
    def setUp(self):
        self.temp_keywords_db = "keywords_db.json"
        # Inicia com algumas keywords
        # Exemplo:
        db = {
            "agendamentos": ["vou agendar", "pode marcar", "marcar", "agendar"],
            "cancelamentos": ["cancelar", "desmarcar", "desistir"],
            "pendencias_medico": ["nota fiscal", "pedido de exame", "laudo"]
        }
        save_keywords_db(db, self.temp_keywords_db)

    def tearDown(self):
        if os.path.exists(self.temp_keywords_db):
            os.remove(self.temp_keywords_db)

    def test_daily_report_real_data(self):
        fetcher = LocalFileFetcher()
        dr = DailyReport(fetcher=fetcher, keywords_file=self.temp_keywords_db)
        result = dr.generate_report()

        print("Relatório real data:", result)
        self.assertIn("agendamentos_realizados", result)
        self.assertIn("cancelamentos_consultas", result)
        self.assertIn("pendencias_ao_medico", result)

        # Ex.: se espera que haja x conversas, pode checar
        # self.assertGreaterEqual(result["total_conversas_hoje"], 1)

if __name__ == "__main__":
    unittest.main()
