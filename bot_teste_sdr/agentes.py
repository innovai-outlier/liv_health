# agentes.py

class Agent:
    def __init__(self, name, role, mode):
        """
        :param name: Nome do agente (ex: "Lead Crítico")
        :param role: "assistente" ou "lead"
        :param mode: "dinamico" ou "estatico"
        """
        self.name = name
        self.role = role
        self.mode = mode
        self.messages = []  # Lista de mensagens trocadas
        self.metrics = {}   # Métricas (para agente-alvo)

    def add_message(self, sender, content):
        """Registra uma mensagem no histórico."""
        self.messages.append({"from": sender, "content": content})

    def get_conversation(self):
        """Retorna o histórico de conversa formatado como string."""
        conv = ""
        for msg in self.messages:
            if msg["from"] == "lead":
                conv += f"Agente: {msg['content']}\n"
            else:
                conv += f"SDR: {msg['content']}\n"
        return conv

class Lead(Agent):
    def __init__(self, name, profile, mode="dinamico"):
        """
        :param profile: Perfil do lead (ex: "critico", "moderado", etc.)
        """
        super().__init__(name, role="lead", mode=mode)
        self.profile = profile

class Assistente(Agent):
    def __init__(self, name, mode="dinamico"):
        super().__init__(name, role="assistente", mode=mode)
