# integration_tests/test_integration_local.py
import unittest
import os
import json
from src.agents.agentes import Lead, Assistente
from src.analysis.analise import (
    avaliar_aptidao_funil,
    avaliar_temperatura_lead,
    avaliar_conversao,
    avaliar_respostas_genericas,
    avaliar_grau_robotizacao,
    avaliar_compreensao_semantica,
    avaliar_adequacao_gramatical,
    avaliar_respeito_encaminhamento,
    avaliar_conhecimento_servicos
)
from src.storage.base_conversas import adicionar_conversa, carregar_conversas
from src.analysis.sinonimos import expandir_sinonimos

TEST_CONVERSAS_FILE = "test_conversas.json"

class TestIntegrationLocalConversation(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_CONVERSAS_FILE):
            os.remove(TEST_CONVERSAS_FILE)
        with open(TEST_CONVERSAS_FILE, "w", encoding="utf-8") as f:
            json.dump({"conversas": []}, f)
        self.lead = Lead(name="Lead_Critico", profile="critico", mode="dinamico")
        self.assistente = Assistente(name="Assistente_Local", mode="dinamico")
        self.novas_palavras = set()
    
    def tearDown(self):
        if os.path.exists(TEST_CONVERSAS_FILE):
            os.remove(TEST_CONVERSAS_FILE)
    
    def test_dynamic_conversation_with_new_models(self):
        num_turnos = 5
        for i in range(num_turnos):
            contexto_lead = self.lead.get_conversation()
            lead_msg = self.lead.gerar_proxima_mensagem(contexto_lead)
            self.lead.add_message("lead", lead_msg)
            contexto_total = self.lead.get_conversation() + self.assistente.get_conversation()
            assist_msg = self.assistente.gerar_proxima_mensagem(contexto_total)
            self.assistente.add_message("assistente", assist_msg)
            for palavra in assist_msg.split():
                self.novas_palavras.add(palavra.lower())
        
        conversa_final = self.lead.get_conversation() + self.assistente.get_conversation()
        print("Conversa Dinâmica Simulada:\n", conversa_final)
        
        aptidao = avaliar_aptidao_funil(conversa_final)
        temperatura = avaliar_temperatura_lead(conversa_final)
        conversao = avaliar_conversao(conversa_final)
        respostas_gen = avaliar_respostas_genericas(conversa_final)
        robotizacao = avaliar_grau_robotizacao(conversa_final)
        comp_semantica = avaliar_compreensao_semantica(conversa_final)
        adequacao = avaliar_adequacao_gramatical(conversa_final)
        respeito = avaliar_respeito_encaminhamento(conversa_final)
        conhecimento = avaliar_conhecimento_servicos(conversa_final)
        
        rotulo_sucesso = True if conversao == "Convertido" else False
        
        metricas = {
            "Aptidão para o Funil": aptidao,
            "Temperatura do Lead": temperatura,
            "Conversão": conversao,
            "Respostas Genéricas (%)": respostas_gen,
            "Grau de Robotização": robotizacao,
            "Compreensão Semântica": comp_semantica,
            "Adequação Gramatical": adequacao,
            "Respeito à Regra de Encaminhamento": respeito,
            "Conhecimento dos Serviços": conhecimento,
            "Sucesso": rotulo_sucesso
        }
        
        conversas_registro = []
        msgs = self.lead.messages + self.assistente.messages
        for idx in range(0, len(msgs), 2):
            item = {"agente": msgs[idx]["content"]}
            if idx + 1 < len(msgs):
                item["assistente"] = msgs[idx+1]["content"]
            conversas_registro.append(item)
        
        registro = {
            "id": "conv_test_001",
            "tipo": "dinamica",
            "mensagens": conversas_registro,
            "metricas": metricas
        }
        
        with open(TEST_CONVERSAS_FILE, "r", encoding="utf-8") as f:
            base = json.load(f)
        base["conversas"].append(registro)
        with open(TEST_CONVERSAS_FILE, "w", encoding="utf-8") as f:
            json.dump(base, f, indent=4, ensure_ascii=False)
        
        with open(TEST_CONVERSAS_FILE, "r", encoding="utf-8") as f:
            base_final = json.load(f)
        self.assertGreaterEqual(len(base_final["conversas"]), 1)
        self.assertTrue(len(conversa_final) > 0)
        
        expandir_sinonimos(self.novas_palavras)
        
        print("\nMétricas Calculadas:")
        for k, v in metricas.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    unittest.main()
