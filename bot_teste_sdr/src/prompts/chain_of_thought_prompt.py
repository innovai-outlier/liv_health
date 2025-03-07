# src/prompts/strategy_chain_of_thought.py

from .base_prompt import BasePrompt

class ChainOfThoughtPrompt(BasePrompt):
    """Implementação de Chain-of-Thought Prompting."""

    def __init__(self):
        super().__init__()
        self.strategy_name = "Chain-of-Thought Prompting"

    def format_prompt(self, conversations):
        messages = [
            {"role": "system", "content": "Você é um assistente que analisa interações entre pacientes e assistentes. "
                                          "Explique seu raciocínio passo a passo antes de gerar a resposta final."}
        ]

        for conv in conversations:
            for msg in conv["mensagens"]:
                role = "user" if msg["from"] == "lead" else "assistant"
                messages.append({"role": role, "content": msg["text"]})

        messages.append(
            {"role": "user", "content": "Agora, pense passo a passo e gere um relatório detalhado baseado nessas conversas."}
        )

        return messages
