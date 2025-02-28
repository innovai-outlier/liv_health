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
        Carrega conversas de um dia específico dentro do diretório da base (train, test ou validate).
        Retorna apenas conversas onde há pelo menos uma mensagem registrada na data desejada.
        """
        all_conversations = []

        for file in os.listdir(base_dir):
            if file.endswith(".json"):
                file_path = os.path.join(base_dir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)  # Agora sabemos que data é uma lista!

                        # Verifica se o JSON contém uma lista
                        if not isinstance(data, list):
                            print(f"⚠️ ERRO: Estrutura inesperada no arquivo {file}. Esperado uma lista de conversas, mas recebeu {type(data)}.")
                            continue

                        # Itera sobre cada conversa na lista
                        for conv in data:
                            if not isinstance(conv, dict):
                                print(f"⚠️ ERRO: Conversa mal formatada no arquivo {file}: esperado dicionário, mas recebeu {type(conv)}.")
                                continue

                            if "mensagens" not in conv or not isinstance(conv["mensagens"], list):
                                print(f"⚠️ ERRO: Estrutura incorreta em {file}. Conversa sem 'mensagens' ou formato inesperado.")
                                continue

                            # 🔍 Filtra mensagens do dia desejado
                            filtered_messages = [msg for msg in conv["mensagens"] if isinstance(msg, dict) and "timestamp" in msg and msg["timestamp"].startswith(target_date)]

                            # Apenas adiciona conversas que tenham mensagens no dia filtrado
                            if filtered_messages:
                                all_conversations.append({
                                    "lead_id": conv.get("lead_id", "desconhecido"),  # Mantém lead_id
                                    "label": conv.get("label", "desconhecido"),  # Mantém rótulo
                                    "mensagens": filtered_messages
                                })

                    except json.JSONDecodeError as e:
                        print(f"⚠️ ERRO: Falha ao decodificar JSON em {file}: {e}")

        print(f"✅ {len(all_conversations)} conversas carregadas para {target_date}.")
        return all_conversations

    def format_prompt(self, conversations):
        """ Formata as conversas em partes menores e alternadas corretamente entre user e assistant """

        messages = [{"role": "system", "content": 
            "Você é um assistente que gera relatórios médicos baseados em interações entre pacientes e assistentes.\n"
            "Vamos gerar um relatório estruturado com base nas interações fornecidas.\n"
        }]

        last_role = "assistant"  # Para garantir alternância correta

        # 🔹 Processa as conversas e alterna corretamente entre user e assistant
        for conv in conversations:
            for msg in conv["mensagens"]:
                role = "user" if msg["from"] == "lead" else "assistant"

                # 🔄 Garante alternância correta
                if role == last_role:
                    continue  

                messages.append({"role": role, "content": msg["text"]})
                last_role = role  # Atualiza último papel

        # 🔹 Alternância garantida nas partes do relatório

        # 🟢 Parte 1: Solicitação do Resumo Analítico
        messages.append({"role": "user", "content":
            "Agora gere o **Resumo Analítico**, listando apenas as ocorrências abaixo:\n"
            "- Quantidade de agendamentos\n"
            "- Origem do atendimento: Google, Instagram, Indicação, Já é paciente\n"
            "- Cancelamentos\n"
            "- Reagendamentos\n"
            "- Conversas em aberto (Assistente não respondeu)\n"
            "- Conversas em aberto (Lead não respondeu)\n"
            "- Pendências ao médico\n"
        })
        messages.append({"role": "assistant", "content": "Gerando o Resumo Analítico com base nos dados recebidos..."})

        # 🔵 Parte 2: Solicitação do Resumo Detalhado
        messages.append({"role": "user", "content":
            "Agora gere o **Resumo Detalhado**, explicando os seguintes pontos:\n"
            "- Motivos do cancelamento\n"
            "- Motivos do reagendamento\n"
        })
        messages.append({"role": "assistant", "content": "Gerando o Resumo Detalhado, analisando os motivos mencionados..."})

        # 🔴 Parte 3: Solicitação das Pendências ao Médico
        messages.append({"role": "user", "content":
            "Por fim, relacione as pendências ao médico, incluindo o **ID do lead (número de telefone)** e sua pendência específica.\n"
            "Considere todas as interações fornecidas."
        })
        #messages.append({"role": "assistant", "content": "Listando todas as pendências ao médico identificadas..."})

        return messages


    def generate_report(self, conversations, max_tokens=512):
        """ Gera um relatório diário baseado na IA generativa """

        if not conversations:
            return {"gerado_por": "IA Generativa", "resumo": "Nenhuma conversa encontrada para esta data."}

        # Formata o prompt corretamente
        messages = self.format_prompt(conversations)
        
        # Definir manualmente o token de padding
        self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        self.tokenizer.pad_token_id = self.tokenizer.eos_token_id or self.tokenizer.pad_token_id

        # Aplica o template de chat para tokenização correta
        model_inputs = self.tokenizer.apply_chat_template(messages, return_tensors="pt", padding=True).to(self.device)    
        
        # Criar a máscara de atenção
        attention_mask = model_inputs.ne(self.tokenizer.pad_token_id).long()

        # 🔍 Geração do texto (corrigido)
        generated_ids = self.model.generate(
            model_inputs,
            max_new_tokens=max_tokens,
            attention_mask=attention_mask,  # ✅ Adicionado para evitar comportamento inesperado
            pad_token_id=self.tokenizer.eos_token_id  # ✅ Evita avisos sobre padding
        )

        # Decodifica o texto gerado
        report_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)

        return {"gerado_por": "IA Generativa", "resumo": report_text}