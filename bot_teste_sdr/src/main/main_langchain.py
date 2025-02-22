# src/main/main_langchain.py
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryMemory
from src.config.papeis_config import carregar_modelos

def main():
    config = carregar_modelos()
    llm_assistente = HuggingFacePipeline(
        pipeline=config["assistente"],
        model_kwargs=config["assistente_params"]
    )
    prompt_template = PromptTemplate(
        input_variables=["history", "input"],
        template="""Contexto da conversa:
{history}

Pergunta: {input}
Resposta:"""
    )
    memory = ConversationSummaryMemory(
        llm=llm_assistente,
        memory_key="history",
        input_key="input",
        max_token_limit=1024
    )
    chain_assistente = LLMChain(
        llm=llm_assistente,
        prompt=prompt_template,
        memory=memory
    )
    user_input = "Olá, quero agendar um atendimento com a clínica."
    response = chain_assistente.run(input=user_input)
    print("Resposta do Assistente:", response)

if __name__ == "__main__":
    main()
