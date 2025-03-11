# src/prompts/conversational_prompt.py

from src.prompts.base_prompt import BasePrompt

class ConversationalPrompt(BasePrompt):
    """Prompt que ensina progressivamente o modelo e reforça a geração do JSON correto."""

    def __init__(self):
        self.strategy_name = "Conversacional"

    def format_prompt(self, conversations):
        """Constrói um prompt interativo, explicando todas as métricas e garantindo a resposta JSON."""

        messages = [
            {"role": "system", "content": "Você é um assistente especializado em análise de interações entre pacientes e assistentes. "
                                          "Vamos praticar primeiro para garantir que você compreende bem cada métrica."},
            {"role": "user", "content": "Vou explicar algumas métricas e testar seu entendimento. No final, gere um JSON estruturado com todas as métricas extraídas."},

            # Explicação de todas as métricas antes de pedir a geração do JSON
            {"role": "user", "content": "📝 **Agendamentos**: Sempre que um lead confirmar um horário e a assistente validar, isso conta como um agendamento.\n"
                                        "🗑️ **Cancelamentos**: Sempre que um lead desistir de um agendamento confirmado, contamos como um cancelamento.\n"
                                        "🔄 **Reagendamentos**: Se um lead cancelar e marcar um novo horário, isso conta como um reagendamento.\n"
                                        "📢 **Origem do Atendimento**: Se o lead mencionar que veio do Google, Instagram, Indicação ou já é paciente, registre corretamente.\n"
                                        "🚨 **Leads sem Atendimento**: Se o lead mandou mensagens, mas a assistente não respondeu, liste o ID.\n"
                                        "🛑 **Leads Inertes**: Se o lead recebeu resposta, mas nunca continuou a conversa, liste o ID.\n"
                                        "📌 **Pendências ao Médico**: Se o lead pediu algo como nota fiscal ou receita e a assistente não respondeu, registre.\n"
                                        "⏳ **Tempo Máximo de Resposta**: Para cada lead, calcule o maior tempo que a assistente demorou para responder.\n"},

            # Aplicação nas conversas reais
            {"role": "user", "content": "Agora, analise as seguintes conversas:"},
            {"role": "user", "content": conversations},
            {"role": "user", "content": "Agora, gere um JSON com TODAS as métricas corretamente preenchidas no seguinte formato:"},
            {"role": "user", "content":
                """{
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
                }"""
            }
        ]

        return messages
