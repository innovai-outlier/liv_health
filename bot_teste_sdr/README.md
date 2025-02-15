# Assistente Virtual – Auditoria & Aprendizado Contínuo

Este framework permite auditar uma assistente virtual através de duas abordagens:
- **Dinâmica:** Gera leads simulados (dinamicamente) e coleta conversas em tempo real.
- **Estática:** Utiliza uma base de conversas pré-gravadas para calcular métricas e comparar resultados.

O framework organiza os agentes em uma hierarquia:  
- **Agente-Alvo (Assistente):** O objeto a ser auditado (inclui métricas).
- **Agente de Teste (Lead):** Simula o comportamento dos leads (perfil: crítico, moderado, etc.).

## Funcionalidades

- **Métricas de desempenho:**  
  - Aptidão para o Funil  
  - Temperatura do Lead (1-10)  
  - Conversão  
  - Respostas Genéricas (%)  
  - Grau de Robotização (0-10)  
  - Compreensão Semântica  
  - Adequação Gramatical  
  - Respeito à Regra de Encaminhamento  
  - Conhecimento dos Serviços

- **Aprendizado contínuo:** A base de sinônimos é expandida automaticamente com novas palavras identificadas em cada auditoria.
- **Gerenciamento histórico:** Conversas (mensagens) são armazenadas em uma base para auditorias estáticas futuras, com rótulos de métricas.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
3. Execute o script principal (escolha o tipo de auditoria):
   ```bash
   python main.py --tipo dinamica
   # ou para auditoria estática:
   python main.py --tipo estatica
  
## 🧪 Testes Unitários

Para garantir que o framework funcione corretamente e detectar possíveis alterações na estrutura da página (por exemplo, se os seletores do WhatsApp Web mudarem), criamos uma suíte de testes unitários.

### Como Executar os Testes

1. Certifique-se de ter todas as dependências instaladas (veja `requirements.txt`).
2. Na raiz do projeto, execute o seguinte comando:
   ```bash
   python -m unittest discover -s tests
