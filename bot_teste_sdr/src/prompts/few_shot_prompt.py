# src/prompts/strategy_few_shot.py

from .base_prompt import BasePrompt

class FewShotPrompt(BasePrompt):
    """Implementação de Few-Shot Prompting."""

    def __init__(self):
        super().__init__()
        self.strategy_name = "Few-Shot Prompting"

    def format_prompt(self, conversations):
        messages = [
            {"role": "system", "content": "Você é um assistente que gera relatórios médicos."},
            {"role": "user", "content": "Aqui está um exemplo de um relatório bem estruturado:"},
            {"role": "assistant", "content": "Relatório de exemplo com métricas e análise..."},
            {"role": "user", "content": "Agora gere um relatório semelhante baseado nas conversas a seguir."}
        ]

        for conv in conversations:
            for msg in conv["mensagens"]:
                role = "user" if msg["from"] == "lead" else "assistant"
                messages.append({"role": role, "content": msg["text"]})

        return messages
