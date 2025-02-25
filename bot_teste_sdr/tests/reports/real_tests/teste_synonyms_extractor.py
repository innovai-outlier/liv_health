# tests/reports/real_data_tests/test_synonyms_extractor.py
import unittest
import os
from unittest.mock import patch

from src.reports.synonyms_extractor import SynonymsExtractor
from src.reports.synonyms_utils import load_synonyms_db, save_synonyms_db

class TestSynonymsExtractorReal(unittest.TestCase):
    def setUp(self):
        self.temp_db_path = "temp_synonyms_db.json"
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

        # Inicia com algo
        db = {
            "nota fiscal": ["nota", "nf"],
            "pendentes": []
        }
        save_synonyms_db(db, self.temp_db_path)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    @patch("builtins.input", side_effect=["y", "n"])
    def test_integrate_pendentes(self, mock_input):
        # Cria synonyms_extractor e simula tokens pendentes
        extr = SynonymsExtractor(path=self.temp_db_path)
        extr.db["pendentes"] = ["notinha", "examezito"]

        # Chama integrate_pendentes => user input: first => 'y', second => 'n'
        extr.integrate_pendentes("nota fiscal")

        new_db = load_synonyms_db(self.temp_db_path)
        # Verifica se 'notinha' foi movido (res='y') e 'examezito' continua em pendentes
        self.assertIn("notinha", new_db["nota fiscal"])
        self.assertIn("examezito", new_db["pendentes"])
        self.assertNotIn("examezito", new_db["nota fiscal"])

        print("After integrate_pendentes =>", new_db)

if __name__ == "__main__":
    unittest.main()
