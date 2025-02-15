import unittest
from analise import (avaliar_aptidao_funil, avaliar_temperatura_lead, avaliar_conversao,
                     avaliar_respostas_genericas, avaliar_grau_robotizacao,
                     avaliar_compreensao_semantica, avaliar_adequacao_gramatical,
                     avaliar_respeito_encaminhamento, avaliar_conhecimento_servicos)

class TestAnaliseFunctions(unittest.TestCase):
    def setUp(self):
        # Exemplo de conversa com alta intenção de agendamento (lead "quente")
        self.conversa_alta = (
            "Agente: Quero agendar uma consulta imediatamente.\n"
            "SDR: Claro, vamos agendar. Por favor, informe seu horário preferido.\n"
            "Agente: Prefiro amanhã de manhã.\n"
            "SDR: Agendamento confirmado para amanhã às 9h."
        )
        # Exemplo de conversa com pouca intenção (lead "frio")
        self.conversa_baixa = (
            "Agente: Estou apenas pesquisando opções.\n"
            "SDR: Posso ajudar, me fale mais sobre o que procura.\n"
            "Agente: Vou pensar.\n"
            "SDR: Entendi, se precisar de algo, estamos à disposição."
        )
    
    def test_aptidao_funil(self):
        self.assertEqual(avaliar_aptidao_funil(self.conversa_alta), "Alta")
        self.assertEqual(avaliar_aptidao_funil(self.conversa_baixa), "Baixa")

    def test_temperatura_lead(self):
        temp_alta = avaliar_temperatura_lead(self.conversa_alta)
        self.assertTrue(7 <= temp_alta <= 10)
        temp_baixa = avaliar_temperatura_lead(self.conversa_baixa)
        self.assertTrue(1 <= temp_baixa <= 6)

    def test_conversao(self):
        self.assertEqual(avaliar_conversao(self.conversa_alta), "Convertido")
        self.assertEqual(avaliar_conversao(self.conversa_baixa), "Não Convertido")
    
    def test_respostas_genericas(self):
        percent_gen = avaliar_respostas_genericas(self.conversa_baixa)
        self.assertTrue(0 <= percent_gen <= 100)
    
    def test_grau_robotizacao(self):
        grau = avaliar_grau_robotizacao(self.conversa_alta)
        self.assertTrue(0 <= grau <= 10)

    def test_compreensao_semantica(self):
        comp = avaliar_compreensao_semantica(self.conversa_alta)
        self.assertTrue(0 <= comp <= 1.0)

    def test_adequacao_gramatical(self):
        adeq = avaliar_adequacao_gramatical(self.conversa_alta)
        self.assertTrue(0 <= adeq <= 1.0)
    
    def test_respeito_encaminhamento(self):
        res = avaliar_respeito_encaminhamento(self.conversa_alta)
        self.assertTrue(0 <= res <= 1.0)
    
    def test_conhecimento_servicos(self):
        conh = avaliar_conhecimento_servicos(self.conversa_alta)
        self.assertTrue(0 <= conh <= 1.0)

if __name__ == "__main__":
    unittest.main()
