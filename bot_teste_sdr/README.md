# Framework de Auditoria de Assistente Virtual

Este projeto é um framework modular e open source para **auditar** o desempenho de uma assistente virtual em cenários de **atendimento** e **agendamento**, rodando **localmente** e usando ferramentas como **LangChain** para gerenciar o **contexto** da conversa sem ultrapassar limites de tokens.

---

## Funcionalidades

1. **Configuração e Sumarização de Prompt**  
   - Em `papeis_config.py`, carregamos a lista de **blocos** de prompt do assistente a partir de um arquivo JSON (por padrão, `assets/assistant_prompt.json`).  
   - Esse arquivo contém vários **chunks** autocontidos que, juntos, formam o texto completo de instruções e diretrizes para a assistente.  
   - Cada chunk evita exceder ~1024 tokens e mantém um contexto coeso (não há cortes de parágrafos no meio).  
   - O framework decide, em `agentes.py`, **como** e **quando** concatenar ou aplicar cada chunk na geração de mensagens.

2. **Definição de Agentes (Lead e Assistente)**  
   - As classes `Agent`, `Lead` e `Assistente` definem como o lead (usuário/paciente) e a assistente se comportam.  
   - O **Lead** pode emitir mensagens de teste, simulando diferentes perfis (crítico, moderado etc.).  
   - A **Assistente** utiliza o prompt carregado em blocos para responder conforme as diretrizes do texto original (ex.: não confirmar agendamentos, usar SPIN Selling, etc.).

3. **Análise de Métricas**  
   - O módulo `src/analysis/analise.py` oferece funções para avaliar vários indicadores de desempenho, como aptidão para o funil, temperatura do lead, conversão etc.  
   - Há também o módulo `src/analysis/sinonimos.py` para manutenção e expansão de sinônimos usando fuzzy matching.

4. **Gerenciamento de Histórico (Base de Conversas)**  
   - Em `src/storage/base_conversas.py`, o framework pode armazenar conversas e métricas em JSON, permitindo auditorias estáticas (reaproveitando logs existentes) ou dinâmicas (gerando conversas em tempo real).

5. **Integração com Selenium**  
   - `src/interface/selenium_bot.py` implementa automação de testes de interface, por exemplo, WhatsApp Web ou páginas de formulário dummy, simulando trocas de mensagens.

6. **Integração com LangChain**  
   - Em `src/main/main_langchain.py`, há um exemplo de uso de `ConversationSummaryMemory` do LangChain para gerenciar o contexto, resumir interações longas e evitar ultrapassar limites de tokens.

---

## Como o Prompt do Assistente Foi Preparado

Para evitar um único arquivo de texto muito grande e sujeito a cortes no meio de contextos importantes, o prompt da assistente foi **fragmentado** em blocos **autocontidos** (chunks). Cada chunk:

- Garante um **tamanho seguro** (bem abaixo de 1024 tokens) e não corta parágrafos ou ideias no meio.
- É armazenado no arquivo JSON `assets/assistant_prompt.json` sob a chave `"assistant_prompt_chunks"`.
- No `papis_config.py`, a função `load_prompt_chunks()` carrega esses blocos, e eles são disponibilizados em `"assistant_prompt_chunks"` no dicionário retornado por `carregar_modelos()`.
- A classe `Assistente` (em `src/agents/agentes.py`) decide como concatenar ou aplicar cada chunk durante a geração de mensagens. Esse método facilita a personalização — você pode concatenar todos os blocos, usar apenas alguns ou criar lógica específica para cada fase da conversa.

Exemplo simplificado do JSON:

```json
{
  "assistant_prompt_chunks": [
    {
      "id": 1,
      "content": "Bloco 1 do prompt..."
    },
    {
      "id": 2,
      "content": "Bloco 2 do prompt..."
    }
  ]
}
```

Essa abordagem mantém o prompt **organizado**, **estruturado** e **pronto** para cenários que exigem limites rígidos de tokens (como integrações com modelos de linguagem).

---

## Instalação e Configuração

### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

### 2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Configure os Arquivos de Assets:

- `assets/assistant_prompt.json`: Contém os blocos do prompt da assistente.
- `assets/sinonimos.json`: Base de sinônimos (carregada e atualizada automaticamente).

---

## Uso

### Execução Básica (Sem LangChain)

```bash
python src/main/main.py
```
- Cria instâncias de `Lead` e `Assistente`.
- Gera mensagens alternadas.
- Ao final, exibe o histórico completo no console.

### Execução com LangChain

```bash
python src/main/main_langchain.py
```
- Carrega os blocos do prompt.
- Configura `LLMChain` com `ConversationSummaryMemory`.
- Simula interação de teste, exibindo a resposta gerada.

---

## Testes

### Testes Unitários
```bash
python -m unittest discover -s tests/unit_tests
```

### Testes de Integração
```bash
python -m unittest discover -s tests/integration_tests
```

---

## Considerações Adicionais

- **Modelos Leves**:  
  Utiliza `EleutherAI/gpt-neo-125M` e `distilgpt2` para execução local. Você pode trocar por modelos mais robustos se tiver recursos de GPU.

- **Gerenciamento de Contexto**:  
  LangChain e técnicas de truncamento/sumarização ajudam a manter conversas longas sem exceder os limites de tokens.

- **Prompt da Assistente**:  
  Agora fragmentado em blocos JSON, facilitando o uso seletivo ou concatenado, sem arriscar cortes abruptos de contexto.

---

## Licença

Este projeto está licenciado sob a licença [MIT](LICENSE).

---

## Contribuições

Sinta-se à vontade para abrir issues ou enviar pull requests. Toda ajuda é bem-vinda no aprimoramento deste framework!

