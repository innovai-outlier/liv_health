import os, re
import json
import openai
from src.prompts.prompt_manager import PromptManager
from src.config import OPENAI_API_KEY

class GenerativeReportGenerator:
    """ Classe para gerar relatório diário baseado em IA generativa """

    def __init__(self, model_name="gpt-4-turbo", prompt_strategy="few_shot"):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.model_name = model_name
        self.prompt_manager = PromptManager(strategy=prompt_strategy)

    
    def extract_json_model_output(self, response):
        """Filtra e extrai apenas o JSON da resposta do modelo"""
        match = re.search(r"\{.*\}", response, re.DOTALL)  # Captura tudo entre {}
        if match:
            try:
                return json.loads(match.group(0))  # Converte para JSON
            except json.JSONDecodeError:
                return {"erro": "Falha ao processar a resposta do modelo. JSON inválido."}
        return {"erro": "Nenhum JSON encontrado na resposta do modelo."}
    
    def generate_report(self, conversations):
        """ Gera um relatório diário baseado no GPT-4 da OpenAI """

        if not conversations:
            return {"gerado_por": "IA Generativa", "resumo": "Nenhuma conversa encontrada para esta data."}

        # Formata o prompt corretamente
        #messages = self.format_prompt(conversations)
        messages = self.prompt_manager.generate_prompt(conversations)  
        
        # Chama a API da OpenAI para gerar o relatório
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.2
        )

        # ✅ Obtém a resposta do modelo
        model_response = response.choices[0].message.content
        report_json = self.extract_json_model_output(model_response)
        print("##############################################")
        print("######### RESPOSTA DIRETA DO MODELO ##########")
        print("##############################################")
        print(model_response)
        
        print("################################################")
        print("######### RESPOSTA FILTRADA DO MODELO ##########")
        print("################################################")
        print(report_json)
        print("################################################")
        print("################################################")
        
        return {"gerado_por": "GPT-4", "resumo": report_json}
