# tests/reports/test_keyword_extractor.py
import unittest
import os, json
from src.reports.keyword_extractor import KeywordExtractor

class TestKeywordExtractor(unittest.TestCase):
    def setUp(self):
        self.temp_keywords_file = "temp_keywords_db.json"
        if os.path.exists(self.temp_keywords_file):
            os.remove(self.temp_keywords_file)
        # Aqui criamos manualmente um dicionário
        db = { "agendou": [], "nao_agendou": [] }
        with open(self.temp_keywords_file, "w", encoding="utf-8") as f:
            json.dump(db, f)

    def tearDown(self):
        if os.path.exists(self.temp_keywords_file):
            os.remove(self.temp_keywords_file)

    def test_process_labeled_history(self):
        # Precisamos de um chatbase mock? 
        # Exemplo de sem chat, so checar se nao crasha
        ke = KeywordExtractor(keywords_file=self.temp_keywords_file)
        result = ke.process_labeled_history(base_dir="test_chatbase")  # Dir fictício
        # Mesmo que não encontre nada, não deve quebrar
        self.assertIn("agendou", result)

if __name__ == "__main__":
    unittest.main()
