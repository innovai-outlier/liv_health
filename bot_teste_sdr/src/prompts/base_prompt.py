# src/prompts/base_prompt.py

from abc import ABC, abstractmethod

class BasePrompt(ABC):
    """Classe base para diferentes estratégias de prompting."""

    def __init__(self):
        self.strategy_name = "Base"  # Nome da estratégia (será sobrescrito nas subclasses)
        self.json_structure = {
            "quantidade_agendamentos": "X",
            "origem_atendimento": {
                "Google": "X",
                "Instagram": "X",
                "Indicação": "X",
                "Já é paciente": "X"
            },
            "cancelamentos": "X",
            "reagendamentos": "X",
            "leads_sem_atendimento": ["ID1", "ID2"],
            "leads_inertes": ["ID1", "ID2"],
            "pendencias_ao_medico": {
                "ID do Lead": "Descrição"
            },
            "motivos_cancelamento": {
                "ID do Lead": "Motivo"
            },
            "motivos_reagendamento": {
                "ID do Lead": "Motivo"
            },
            "tempo_maximo_resposta": {
                "ID do Lead": "X horas, Y minutos"
            }
        }


    @abstractmethod
    def format_prompt(self, conversations):
        """Cada estratégia deve implementar sua própria lógica de formatação de prompt."""
        pass
