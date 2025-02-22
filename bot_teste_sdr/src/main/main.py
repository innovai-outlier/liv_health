# src/main/main.py
from src.agents.agentes import Lead, Assistente

def main():
    lead = Lead("Lead_Critico", "critico", mode="dinamico")
    assistente = Assistente("Assistente_Local", mode="dinamico")
    
    # Simula 3 interações
    for i in range(3):
        lead_msg = lead.gerar_proxima_mensagem(lead.get_conversation())
        lead.add_message("lead", lead_msg)

        context_total = lead.get_conversation() + assistente.get_conversation()
        assist_msg = assistente.gerar_proxima_mensagem(context_total)
        assistente.add_message("assistente", assist_msg)
    
    print("Conversa Completa:")
    print(lead.get_conversation() + assistente.get_conversation())

if __name__ == "__main__":
    main()
