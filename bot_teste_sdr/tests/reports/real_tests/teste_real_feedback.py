import unittest
import os
import json
from src.reports.daily_report import DailyReport
from src.reports.apply_feedback import apply_feedback
from src.reports.fetcher_base import ConversationsFetcher

class LocalFileFetcher(ConversationsFetcher):
    """Mock de conversas baseado na base real armazenada em `assets/chatbase/`"""
    
    def fetch_today_conversations(self):
        with open("assets/chatbase/daily_report.json", "r", encoding="utf-8") as file:
            return json.load(file)

class TestRealFeedback(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        self.temp_report_file = "test_daily_report.json"
        self.temp_feedback_file = "test_feedback.json"

        # Criar relatório simulado
        sample_report = {
            "data": "2025-02-24",
            "total_conversas_hoje": 8,
            "agendamentos_realizados": 5,
            "cancelamentos_consultas": 0,
            "pendencias_ao_medico": 1,
            "detalhes": [
                {"lead_id": "111", "agendamentos_detectados": 1, "pendencias_detectadas": 0},
                {"lead_id": "222", "agendamentos_detectados": 0, "pendencias_detectadas": 1}
            ]
        }
        with open(self.temp_report_file, "w", encoding="utf-8") as file:
            json.dump(sample_report, file, indent=4)

        # Criar feedback humano simulado
        sample_feedback = {
            "status": "approved",
            "comentarios": "Os cancelamentos não foram detectados corretamente.",
            "ajustes": [
                {"lead_id": "222", "campo": "cancelamentos_detectados", "valor_corrigido": 1}
            ]
        }
        with open(self.temp_feedback_file, "w", encoding="utf-8") as file:
            json.dump(sample_feedback, file, indent=4)

    def tearDown(self):
        """Limpeza dos arquivos de teste"""
        if os.path.exists(self.temp_report_file):
            os.remove(self.temp_report_file)
        if os.path.exists(self.temp_feedback_file):
            os.remove(self.temp_feedback_file)

    def test_apply_feedback(self):
        """Testa se o feedback humano foi aplicado corretamente"""
        apply_feedback(self.temp_report_file, self.temp_feedback_file)

        with open(self.temp_report_file, "r", encoding="utf-8") as file:
            updated_report = json.load(file)

        # Verifica se o ajuste foi aplicado corretamente
        for ajuste in updated_report["detalhes"]:
            if ajuste["lead_id"] == "222":
                self.assertEqual(ajuste["cancelamentos_detectados"], 1)

    def test_generate_report_with_feedback(self):
        """Testa a geração do relatório já com feedback aplicado"""
        fetcher = LocalFileFetcher()
        dr = DailyReport(fetcher=fetcher, model_store="model_store.json")
        result = dr.generate_report()

        # Simula aplicação de feedback
        apply_feedback(result, self.temp_feedback_file)

        # Testa se o campo corrigido aparece no relatório atualizado
        for ajuste in result["detalhes"]:
            if ajuste["lead_id"] == "222":
                self.assertEqual(ajuste["cancelamentos_detectados"], 1)

if __name__ == "__main__":
    unittest.main()
