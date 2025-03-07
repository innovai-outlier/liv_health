# src/prompts/base_prompt.py

from abc import ABC, abstractmethod

class BasePrompt(ABC):
    """Classe base para diferentes estratégias de prompting."""

    def __init__(self):
        self.strategy_name = "Base"  # Nome da estratégia (será sobrescrito nas subclasses)

    @abstractmethod
    def format_prompt(self, conversations):
        """Cada estratégia deve implementar sua própria lógica de formatação de prompt."""
        pass
