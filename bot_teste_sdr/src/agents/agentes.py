# src/agents/agentes.py
from src.config.papeis_config import carregar_modelos

config = carregar_modelos()
assistant_chunks = config["assistant_prompt_chunks"]  # Lista de blocos
assistant_model = config["assistente_model"]
assistant_params = config["assistente_params"]
lead_model = config["lead_model"]
lead_params = config["lead_params"]

def truncate_context(context, max_chars=1000):
    if len(context) > max_chars:
        return context[-max_chars:]
    return context

class Agent:
    def __init__(self, name, role, mode):
        self.name = name
        self.role = role  # "lead" ou "assistente"
        self.mode = mode  # "dinamico" ou "estatico"
        self.messages = []
        self.metrics = {}

    def add_message(self, sender, content):
        self.messages.append({"from": sender, "content": content})

    def get_conversation(self):
        conv = ""
        for msg in self.messages:
            if msg["from"] == "lead":
                conv += f"Agente: {msg['content']}\n"
            else:
                conv += f"SDR: {msg['content']}\n"
        return conv

    def gerar_proxima_mensagem(self, context=""):
        # Este método é genérico. Se for "lead" ou "assistente", ajusta a pipeline.
        if self.mode != "dinamico":
            return None
        context = truncate_context(context, max_chars=1000)
        if self.role == "lead":
            prompt = f"{'Lead Prompt aqui...'}\nContexto: {context}\nResposta:"
            generated = lead_model(prompt, **lead_params)
        elif self.role == "assistente":
            # Exemplo simples: pega CHUNK 1 (id=1) e concatena com o contexto
            # ou combine todos os chunks, etc. Fica ao seu critério:
            chunk_text = "\n".join(ch["content"] for ch in assistant_chunks)
            prompt = f"{chunk_text}\n\nContexto: {context}\nResposta:"
            generated = assistant_model(prompt, **assistant_params)
        else:
            return None
        return generated[0]["generated_text"].strip()

class Lead(Agent):
    def __init__(self, name, profile, mode="dinamico"):
        super().__init__(name, role="lead", mode=mode)
        self.profile = profile

class Assistente(Agent):
    def __init__(self, name, mode="dinamico"):
        super().__init__(name, role="assistente", mode=mode)
