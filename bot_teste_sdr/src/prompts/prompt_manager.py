import json
from src.prompts.base_prompt import BasePrompt
from src.prompts.few_shot_prompt import FewShotPrompt
from src.prompts.json_prompt import JSONPrompt
from src.prompts.conversational_prompt import ConversationalPrompt

class PromptManager:
    """Gerencia diferentes estratégias de prompts e fornece a melhor opção conforme a necessidade."""

    def __init__(self, strategy="few_shot"):
        """
        Inicializa o gerenciador de prompts.
        
        :param strategy: Define qual estratégia será utilizada (few_shot, json, conversational).
        """
        self.strategy = strategy
        self.prompt_instance = self._get_prompt_instance()

    def _get_prompt_instance(self):
        """Retorna a instância correta do prompt baseado na estratégia escolhida."""
        if self.strategy == "few_shot":
            return FewShotPrompt()
        elif self.strategy == "json":
            return JSONPrompt()
        elif self.strategy == "conversational":
            return ConversationalPrompt()
        else:
            raise ValueError(f"Estratégia de prompt '{self.strategy}' não reconhecida.")

    def generate_prompt(self, conversations):
        """
        Gera um prompt com base na estratégia escolhida.

        :param conversations: Conversas a serem analisadas.
        :return: Lista estruturada de mensagens para o modelo de IA.
        """
        return self.prompt_instance.format_prompt(conversations)

    def list_available_strategies(self):
        """Retorna as estratégias disponíveis."""
        return ["few_shot", "json", "conversational"]
