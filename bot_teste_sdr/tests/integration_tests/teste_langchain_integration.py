# integration_tests/test_langchain_integration.py
import unittest
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryMemory
from src.config.papeis_config import carregar_modelos

class TestLangChainIntegration(unittest.TestCase):
    def setUp(self):
        self.config = carregar_modelos()
        self.llm_assistente = HuggingFacePipeline(
            pipeline=self.config["assistente"],
            model_kwargs=self.config["assistente_params"]
        )
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template="""Contexto da conversa:
{history}

Pergunta: {input}
Resposta:"""
        )
        self.memory = ConversationSummaryMemory(
            llm=self.llm_assistente,
            memory_key="history",
            input_key="input",
            max_token_limit=1024
        )
        self.chain_assistente = LLMChain(
            llm=self.llm_assistente,
            prompt=self.prompt_template,
            memory=self.memory
        )
        
    def test_conversation_flow(self):
        user_inputs = [
            "Olá, quero agendar um atendimento com a clínica.",
            "Prefiro amanhã de manhã, se possível.",
            "Gostaria de saber mais sobre os serviços oferecidos."
        ]
        
        for inp in user_inputs:
            response = self.chain_assistente.run(input=inp)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0, f"Resposta vazia para input: {inp}")
            memory_vars = self.chain_assistente.memory.load_memory_variables({"input": inp})
            print("Input:", inp)
            print("Response:", response)
            print("Memory:", memory_vars.get("history", ""))
            print("-----")
        
if __name__ == "__main__":
    unittest.main()
