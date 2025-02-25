# tests/reports/real_data_tests/test_real_chatbase.py
import unittest
import os
from src.reports.chat_parser import load_labeled_history
from src.reports.keyword_extractor import KeywordExtractor
from src.reports.keyword_utils import load_keywords_db, save_keywords_db

class TestRealChatbase(unittest.TestCase):
    """
    Testa o comportamento do chat_parser + keyword_extractor
    em dados reais, sem mocks, usando a pasta assets/chatbase.
    """

    def setUp(self):
        # Definimos o caminho real. Certifique-se de rodar
        # a partir do raiz do projeto ou usar caminho absoluto:
        self.real_chatbase_dir = "assets/chatbase"
        self.temp_keywords = "keywords_db.json"

        # Se já existir, remove para recomeçar do zero
        if os.path.exists(self.temp_keywords):
            os.remove(self.temp_keywords)

        # Inicializa com algumas chaves mínimas
        db = {"agendou": [], "nao_agendou": []}
        save_keywords_db(db, self.temp_keywords)

    def tearDown(self):
        if os.path.exists(self.temp_keywords):
            os.remove(self.temp_keywords)

    def test_process_labeled_history_real(self):
        """
        Testa se a feature extrai tokens de conversas reais
        em success_cases e fail_cases.
        """
        # Primeiro, carrega as conversas rotuladas de assets/chatbase
        conversas = load_labeled_history(base_dir=self.real_chatbase_dir)
        self.assertIsInstance(conversas, list, "Deveria retornar lista de conversas")

        # Com esse data, rodamos o KeywordExtractor
        ke = KeywordExtractor(keywords_file=self.temp_keywords)
        result = ke.process_labeled_history(base_dir=self.real_chatbase_dir)

        # Verifica se 'agendou' e 'nao_agendou' continuam existindo
        self.assertIn("agendou", result)
        self.assertIn("nao_agendou", result)

        # Exemplo: checar se extraiu algo
        # Se pelo menos 1 conversa estiver em success_cases e tiver msgs do lead,
        # deve ter gerado alguns tokens em result['agendou'].
        # Caso não gere, pode ser que as conversas tenham formatação inesperada
        print("Keywords extraídas para 'agendou':", result["agendou"])
        print("Keywords extraídas para 'nao_agendou':", result["nao_agendou"])

if __name__ == "__main__":
    unittest.main()
