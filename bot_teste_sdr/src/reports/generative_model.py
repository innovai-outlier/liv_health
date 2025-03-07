import os
import json
import openai
#from src.prompts.prompt_manager import PromptManager
from src.config import OPENAI_API_KEY

class GenerativeReportGenerator:
    """ Classe para gerar relatório diário baseado em IA generativa """

    def __init__(self, model_name="gpt-4-turbo"):
        self.client = openai.OpenAI(api_key="OPENAI_API_KEY")
        self.model_name = model_name
        self.prompt_manager = PromptManager(model_name)

    def load_conversations(self, base_dir="database/test", target_date="2025-01-02", assistente=None):
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
    
    def generate_report(self, conversations):
        """ Gera um relatório diário baseado no GPT-4 da OpenAI """

        if not conversations:
            return {"gerado_por": "IA Generativa", "resumo": "Nenhuma conversa encontrada para esta data."}

        # Formata o prompt corretamente
        #messages = self.format_prompt(conversations)
        messages = self.prompt_manager.get_prompt(conversations)
        
        # Chama a API da OpenAI para gerar o relatório
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.4
        )

        # ✅ Obtém a resposta do modelo
        report_text = response.choices[0].message.content.strip()

        # 🛑 DEBUG: Salva a resposta para análise futura
        with open("debug_gpt_response.txt", "w", encoding="utf-8") as debug_file:
            debug_file.write(report_text)

        # ✅ Tenta converter a resposta diretamente para JSON
        try:
            report_json = json.loads(report_text)
        except json.JSONDecodeError:
            return {
                "gerado_por": "GPT-4",
                "resumo": {"erro": "Falha ao processar a resposta do modelo. Verifique debug_gpt_response.txt para detalhes."}
            }
        
        return {"gerado_por": "GPT-4", "resumo": report_json}
