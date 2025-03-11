# src/prompts/json_format_prompt.py

from src.prompts.base_prompt import BasePrompt

class JSONPrompt(BasePrompt):
    """Prompt que exige que o modelo retorne a resposta diretamente no formato JSON."""

    def __init__(self):
        self.strategy_name = "JSON Format"

    def format_prompt(self, conversations):
        """Constrói um prompt que impõe um formato JSON fixo na resposta."""

        messages = [
            {"role": "system", "content": "Você é um assistente especializado em análise de interações. Retorne **apenas** um JSON válido seguindo este formato."},
            
            {"role": "user", "content": "Analise as seguintes conversas e gere um JSON estruturado contendo:"},
            {"role": "user", "content": conversations},
            {"role": "user", "content": 
                """Agora, gere um JSON com o seguinte formato:
                {
                    "quantidade_agendamentos": X,
                    "origem_atendimento": {"Google": X, "Instagram": X, "Indicação": X, "Já é paciente": X},
                    "cancelamentos": X,
                    "reagendamentos": X,
                    "leads_sem_atendimento": ["ID1", "ID2"],
                    "leads_inertes": ["ID1", "ID2"],
                    "pendencias_ao_medico": {"ID do Lead": "Descrição"},
                    "motivos_cancelamento": {"ID do Lead": "Motivo"},
                    "motivos_reagendamento": {"ID do Lead": "Motivo"},
                    "tempo_maximo_resposta": {"ID do Lead": "X horas, Y minutos"}
                }
                """
            }
        ]

        return messages
