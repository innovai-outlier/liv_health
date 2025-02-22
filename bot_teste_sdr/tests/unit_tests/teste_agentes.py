# unit_tests/test_agentes.py
import unittest
from src.agents.agentes import Agent, Lead, Assistente

class TestAgents(unittest.TestCase):
    def test_agent_message_storage(self):
        agent = Agent("Teste", "lead", "dinamico")
        agent.add_message("lead", "Olá")
        agent.add_message("assistente", "Oi, como posso ajudar?")
        conv = agent.get_conversation()
        self.assertIn("Agente: Olá", conv)
        self.assertIn("SDR: Oi, como posso ajudar?", conv)

    def test_lead_inheritance(self):
        lead = Lead("Lead Crítico", "critico")
        self.assertEqual(lead.role, "lead")
        self.assertEqual(lead.mode, "dinamico")
        self.assertEqual(lead.profile, "critico")

    def test_assistente_inheritance(self):
        assistente = Assistente("Assistente Virtual")
        self.assertEqual(assistente.role, "assistente")
        self.assertEqual(assistente.mode, "dinamico")

if __name__ == "__main__":
    unittest.main()
