from .gpt_prompt import GPTPrompt
from .mistral_prompt import MistralPrompt

class PromptManager:
    def __init__(self, model_name):
        self.model_name = model_name

    def get_prompt(self, conversations):
        """Seleciona o prompt baseado no modelo"""
        if "gpt" in self.model_name.lower():
            return GPTPrompt().format_prompt(conversations)
        elif "mistral" in self.model_name.lower():
            return MistralPrompt().format_prompt(conversations)
        else:
            raise ValueError(f"Modelo {self.model_name} não suportado.")
