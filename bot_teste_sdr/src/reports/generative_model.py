import os
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class GenerativeReportGenerator:
    """ Classe para gerar relatório diário baseado em IA generativa """

    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.2", device="cpu"):
        """ Inicializa o modelo generativo """

        # Configura dispositivo (CPU)
        self.device = torch.device(device)

        # Carrega o modelo e tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=self.device,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )

    def load_conversations(self, base_dir="database/test", target_date="2025-01-02"):
        """
        Carrega conversas de um dia específico dentro do diretório da base (train, test ou validate)
        """
        all_conversations = []
        for file in os.listdir(base_dir):
            if file.endswith(".json"):
                file_path = os.path.join(base_dir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # Filtra mensagens do dia desejado
                    filtered_messages = [msg for msg in data["mensagens"] if msg["timestamp"].startswith(target_date)]
                    
                    if filtered_messages:
                        all_conversations.append({
                            "lead_id": data["lead_id"],
                            "mensagens": filtered_messages
                        })

        return all_conversations

    def format_prompt(self, conversations):
        """ Formata as conversas para serem interpretadas corretamente pelo modelo """

        messages = [{"role": "system", "content": 
            "Você é um assistente que gera relatórios médicos baseados em interações entre pacientes e assistentes.\n"
            "Leia atentamente as interações e gere um resumo diário estruturado contendo:\n"
            "- Quantidade de agendamentos\n"
            "- Cancelamentos\n"
            "- Pendências ao médico\n"
            "Considere todas as interações abaixo para compilar seu relatório."
        }]

        last_role = "assistant"  # Garante que alternamos corretamente

        for conv in conversations:
            for msg in conv["mensagens"]:
                role = "user" if msg["from"] == "lead" else "assistant"

                # 🚀 Garante que sempre alternamos entre "user" e "assistant"
                if role == last_role:
                    continue  # Se for duplicado, pula

                messages.append({"role": role, "content": msg["text"]})
                last_role = role  # Atualiza o último papel

        # Instrução final para gerar o resumo
        messages.append({"role": "user", "content": "Com base nessas interações, gere um resumo detalhado das métricas citadas acima."})

        return messages

    def generate_report(self, conversations, max_tokens=512):
        """ Gera um relatório diário baseado na IA generativa """

        # Carrega conversas do dia específico
        # conversations = self.load_conversations(base_dir, target_date)

        if not conversations:
            return {"gerado_por": "IA Generativa", "resumo": "Nenhuma conversa encontrada para esta data."}

        # Formata o prompt corretamente
        messages = self.format_prompt(conversations)

        # Aplica o template de chat para tokenização correta
        model_inputs = self.tokenizer.apply_chat_template(messages, return_tensors="pt").to(self.device)

        # Geração do texto
        generated_ids = self.model.generate(model_inputs.input_ids, max_new_tokens=max_tokens)

        # Decodifica o texto gerado
        report_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)

        return {"gerado_por": "IA Generativa", "resumo": report_text}
