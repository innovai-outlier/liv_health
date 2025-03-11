# src/prompts/chain_of_thought_prompt.py

from src.prompts.base_prompt import BasePrompt

class ChainOfThoughtPrompt(BasePrompt):
    """Prompt que incentiva o modelo a seguir um raciocínio lógico antes de responder."""

    def __init__(self):
        self.strategy_name = "Chain of Thought"

    def format_prompt(self, conversations):
        """Constrói um prompt que exige pensamento estruturado antes de gerar a resposta final."""

        messages = [
            {"role": "system", "content": "Você é um assistente especializado na análise de interações entre pacientes e assistentes. "
                                        "Vamos analisar cada métrica separadamente antes de gerar um relatório completo."},

            # 🎯 Agendamentos
            {"role": "user", "content": "Se um lead confirmar um horário e a assistente validar, conta como um agendamento. "
                                        "Exemplo:\n"
                                        "Lead: 'Quero marcar na sexta-feira às 15h.'\n"
                                        "Assistente: 'Ótimo! Está confirmado para sexta às 15h!'\n\n"
                                        "Agora, identifique todos os agendamentos nesta conversa:"},

            {"role": "assistant", "content": "Aqui há **um** agendamento para sexta-feira."},

            # 🎯 Cancelamentos e Motivos
            {"role": "user", "content": "Se um lead disser 'Preciso cancelar meu agendamento', isso conta como um cancelamento. "
                                        "Se ele mencionar o motivo, registre-o.\n"
                                        "Agora, identifique os cancelamentos e seus motivos:"},

            {"role": "assistant", "content": "O lead +55 11 98799-1370 cancelou seu agendamento. Motivo: 'Não conseguirei comparecer'."},

            # 🎯 Reagendamentos e Motivos
            {"role": "user", "content": "Se o lead cancelar, mas depois reagendar para outro dia, isso conta como um reagendamento. "
                                        "Registre também o motivo, se houver.\n"
                                        "Agora, identifique os reagendamentos e seus motivos:"},

            {"role": "assistant", "content": "O lead +55 11 98115-4756 reagendou para quinta-feira. Motivo: 'Eu ainda estarei fora'."},

            # 🎯 Origem do Atendimento
            {"role": "user", "content": "Se o lead disser 'Achei a clínica no Google', a origem é Google. "
                                        "Se disser 'Minha amiga recomendou', é Indicação. "
                                        "Agora, identifique todas as origens de atendimento:"},

            {"role": "assistant", "content": "Um lead veio do **Instagram**, e outro já era paciente."},

            # 🎯 Leads sem Atendimento e Leads Inertes
            {"role": "user", "content": "Leads sem atendimento são aqueles que enviaram mensagens, mas nunca receberam resposta. "
                                        "Leads inertes são aqueles que receberam resposta, mas não continuaram a conversa. "
                                        "Agora, identifique os leads sem atendimento e os inertes na conversa:"},

            {"role": "assistant", "content": "O lead +55 11 99999-9999 não foi atendido e deve ser listado como **lead sem atendimento**."},

            # 🎯 Pendências ao Médico
            {"role": "user", "content": "Se um lead pedir nota fiscal ou exames e não receber resposta, ele tem uma pendência ao médico. "
                                        "Agora, identifique as pendências na conversa:"},

            {"role": "assistant", "content": "O lead +55 11 88888-8888 pediu um exame e não recebeu resposta."},

            # 🎯 Tempo Máximo de Resposta
            {"role": "user", "content": "Agora, calcule o tempo máximo de resposta da assistente. "
                                        "Se um lead enviou uma mensagem às 08:00 e a assistente respondeu às 08:10, o tempo máximo foi 10 minutos.\n"
                                        "Agora, calcule os tempos máximos na conversa:"},

            {"role": "assistant", "content": "O lead +55 11 77777-7777 teve um tempo máximo de resposta de **4 horas, 32 minutos**."},

            # ✅ Geração do JSON Final
            {"role": "user", "content": "Agora que entendemos todas as métricas, gere um JSON completo no seguinte formato:"},
            
            {"role": "user", "content": """{
                "quantidade_agendamentos": X,
                "origem_atendimento": {
                    "Google": X,
                    "Instagram": X,
                    "Indicação": X,
                    "Já é paciente": X
                },
                "cancelamentos": X,
                "motivos_cancelamento": {"ID do Lead": "Motivo"},
                "reagendamentos": X,
                "motivos_reagendamento": {"ID do Lead": "Motivo"},
                "leads_sem_atendimento": ["ID1", "ID2"],
                "leads_inertes": ["ID1", "ID2"],
                "pendencias_ao_medico": {"ID do Lead": "Descrição"},
                "tempo_maximo_resposta": {"ID do Lead": "X horas, Y minutos"}
            }"""},

            {"role": "user", "content": "Agora, gere o JSON final baseado nas conversas abaixo."},

            {"role": "user", "content": conversations}
        ]
        return messages
