# unit_tests/test_base_conversas.py
import unittest
import os
import json
from src.storage.base_conversas import adicionar_conversa, carregar_conversas, buscar_conversa_similar

class TestBaseConversas(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_conversas.json"
        self.original_file = "conversas.json"
        if os.path.exists(self.original_file):
            os.rename(self.original_file, self.test_file)
        with open(self.original_file, "w", encoding="utf-8") as f:
            json.dump({"conversas": []}, f)

    def tearDown(self):
        if os.path.exists(self.original_file):
            os.remove(self.original_file)
        if os.path.exists(self.test_file):
            os.rename(self.test_file, self.original_file)

    def test_adicionar_conversa(self):
        mensagens = [{"agente": "Olá", "assistente": "Oi"}]
        metricas = {"Aptidão para o Funil": "Alta"}
        adicionar_conversa("dinamica", mensagens, metricas)
        base = carregar_conversas()
        self.assertEqual(len(base["conversas"]), 1)
        self.assertEqual(base["conversas"][0]["metricas"], metricas)

    def test_buscar_conversa_similar(self):
        mensagens = [{"agente": "Olá, quero agendar uma consulta", "assistente": "Claro, vamos agendar"}]
        metricas = {"Aptidão para o Funil": "Alta"}
        adicionar_conversa("dinamica", mensagens, metricas)
        conv = buscar_conversa_similar("Quero agendar uma consulta")
        self.assertIsNotNone(conv)
        self.assertEqual(conv["metricas"], metricas)

if __name__ == "__main__":
    unittest.main()
