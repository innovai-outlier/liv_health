# src/prompts/strategy_few_shot.py

from .base_prompt import BasePrompt

class FewShotPrompt(BasePrompt):
    """Implementação de Few-Shot Prompting."""

    def __init__(self):
        super().__init__()
        self.strategy_name = "Few-Shot Prompting"

    def format_prompt(self, conversations):
        messages = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": "Você é um assistente especializado na análise de interações entre pacientes e assistentes."},
                    {"type": "text", "text": "Sua tarefa é **exclusivamente** gerar um relatório JSON estruturado."},
                    {"type": "text", "text": "⚠️ **ATENÇÃO:** NÃO inclua explicações, apenas retorne um JSON válido seguindo este formato:"},
                    {"type": "text", "text": str(self.json_structure)}
                ]
            },
            # 🎯 Exemplo 1 - Agendamentos
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Exemplo de conversa:"},
                    {"type": "text", "text": "'lead_id': +55 11 998765432"},
                    {"type": "text", "text": "[10:00] Lead: 'Quero marcar para segunda-feira.'"},
                    {"type": "text", "text": "[10:05] Assistente: 'Segunda às 14h está disponível!'"},
                    {"type": "text", "text": "[10:10] Lead: 'Ótimo, pode marcar!'"},
                    {"type": "text", "text": "[10:15] Assistente: 'Agendamento confirmado!'"},
                    {"type": "text", "text": "Quantos agendamentos há nessa conversa?"}
                ]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "Há **1 agendamento**, pois o lead confirmou e a assistente validou."}]
            },
            # 🎯 Exemplo 2 - Cancelamentos
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Agora veja esse caso:"},
                    {"type": "text", "text": "[11:00] Lead: 'Preciso cancelar minha consulta.'"},
                    {"type": "text", "text": "[11:05] Assistente: 'Cancelamento registrado!'"},
                    {"type": "text", "text": "Quantos cancelamentos foram feitos?"}
                ]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "Há **1 cancelamento**, pois o lead desistiu do agendamento."}]
            },
            # 🎯 Exemplo 3 - Reagendamentos
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "E se o lead cancelar e reagendar?"},
                    {"type": "text", "text": "[12:00] Lead: 'Preciso cancelar minha consulta.'"},
                    {"type": "text", "text": "[12:05] Assistente: 'Cancelamento registrado!'"},
                    {"type": "text", "text": "[12:10] Lead: 'Na verdade, quero remarcar para sexta.'"},
                    {"type": "text", "text": "[12:15] Assistente: 'Agendado para sexta!'"},
                    {"type": "text", "text": "Quantos reagendamentos há?"}
                ]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "Há **1 reagendamento**, pois o compromisso original foi cancelado, mas um novo foi marcado."}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": "E sobre esse reagendamento, o que motivou esse lead?"}]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "O lead não conseguiria na data e hora original por motivos pessoais, e por conta disso preferiu na sexta."}]
            },
            # 🎯 Exemplo 4 - Origem do Atendimento
            {
                "role": "user",
                "content": [{"type": "text", "text": "Se o lead disser 'Achei no Google', qual a origem do atendimento?"}]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "A origem do atendimento é **Google**."}]
            },
            # 🎯 Exemplo 5 - Leads sem atendimento
            {
                "role": "user",
                "content": [{"type": "text", "text": "Se o lead enviar mensagens e não receber resposta, o que acontece?"}]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "Ele deve ser listado como **lead sem atendimento**."}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": "Se o lead enviar mensagens e não receber resposta, além de ficar marcado como lead sem atendimento, o que mais precisa ser feito?"}]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "Deve ser calculado o **tempo máximo de sem resposta** do assistente, em horas/minutos/segundos."}]
            },
            
            # ✅ Geração do JSON Final
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Agora que você aprendeu todas as métricas, gere um JSON completo com base nas conversas abaixo."},
                    {"type": "text", "text": str(conversations)},
                    {"type": "text", "text": "Retorne o JSON no formato especificado anteriormente:"},
                    {"type": "text", "text": str(self.json_structure)}
                ]
            }
        ]
        return messages
