# Framework de Auditoria de Assistente Virtual

Este projeto é um framework modular e open source para **auditar** o desempenho de uma assistente virtual em cenários de **atendimento** e **agendamento**, rodando **localmente** e usando ferramentas como **LangChain** para gerenciar o **contexto** da conversa sem ultrapassar limites de tokens.

---
## Funcionalidades

1. **Configuração e Sumarização de Prompt**  
   - Em `papeis_config.py`, o framework carrega uma lista de blocos (chunks) do prompt da assistente a partir de um arquivo JSON (por padrão, `assets/assistant_prompt.json`).  
   - Cada chunk é autocontido, evitando exceder ~1024 tokens, e preserva a integridade do contexto, sem cortar parágrafos ou ideias.  
   - O framework define, em `agentes.py`, como e quando concatenar ou aplicar esses blocos na geração das mensagens da assistente.

2. **Definição de Agentes (Lead e Assistente)**  
   - As classes `Agent`, `Lead` e `Assistente` modelam o comportamento dos participantes da conversa, simulando perfis variados de leads (por exemplo, crítico, moderado) e as respostas da assistente de acordo com as diretrizes pré-definidas (como o uso de SPIN Selling e a restrição de confirmação de agendamentos).

3. **Análise de Métricas e Auditoria**  
   - O módulo `src/analysis/analise.py` fornece funções para avaliar indicadores de desempenho (aptidão para o funil, temperatura do lead, conversão etc.) e mantém uma base de sinônimos via `src/analysis/sinonimos.py` (utilizando técnicas de fuzzy matching) para enriquecer a análise textual.

4. **Gerenciamento de Histórico (Base de Conversas)**  
   - Em `src/storage/base_conversas.py`, o framework armazena conversas e métricas em formato JSON, possibilitando auditorias tanto estáticas (com logs históricos existentes) quanto dinâmicas (gerando conversas em tempo real).

5. **Integração com Selenium e API**  
   - `src/interface/selenium_bot.py` implementa automação para interagir com plataformas web (por exemplo, WhatsApp Web), simulando a troca de mensagens.  
   - Módulos como `fetcher_selenium.py` e `fetcher_api.py` (na pasta `reports/`) permitem a coleta de conversas via Selenium ou através de chamadas de API, conforme a necessidade.

6. **Processamento via Embeddings e Classificação Multi-Classe**  
   - Com o uso do **Sentence-BERT** (integrado em `src/reports/embeddings_utils.py`), o framework gera embeddings das mensagens dos leads.  
   - O módulo `src/reports/embedding_extractor.py` treina um classificador multi-classe (por exemplo, usando logistic regression) para distinguir entre diferentes rótulos, como “agendou”, “cancelou”, “pendencia” e “nao_agendou”.  
   - Esse classificador permite capturar nuances e variações linguísticas automaticamente, sem depender exclusivamente de listas fixas de palavras-chave.

7. **Expansão Automática de Sinônimos**  
   - Os módulos `src/reports/synonyms_utils.py` e `src/reports/synonyms_extractor.py` trabalham juntos para manter e enriquecer dinamicamente a base de sinônimos.  
   - Se um token novo não corresponder a nenhum sinônimo existente, o método `integrate_pendentes()` pode interativamente (ou via heurística) decidir se esse token deve ser adicionado a uma chave específica, enriquecendo a base.

8. **Geração de Relatório Diário**  
   - Em `src/reports/daily_report.py`, a classe `DailyReport` consolida as conversas coletadas e processadas, integrando a classificação via embeddings e o dicionário de sinônimos para calcular métricas importantes:
     - **Agendamentos realizados:** Leads que demonstraram intenção ou confirmação de agendamento (sem cancelamento posterior).
     - **Cancelamentos:** Casos em que o lead, após ter agendado, desistiu do compromisso.
     - **Pendências direcionadas ao médico:** Situações em que, mesmo após agendamento, o lead solicita algo (por exemplo, nota fiscal, receita, exames) e não recebe a confirmação ou resolução, considerando também se mensagens do assistente indicam que a pendência foi resolvida (por exemplo, com termos como “resolvido”, “enviado”, “emitido”).
   - O relatório é gerado combinando os dados do fetcher com as predições do classificador e a análise dos sinônimos, proporcionando uma visão detalhada de cada conversa.

---

## Formas de Execução

- **Execução dos Scripts em `main/`:**
  - `python src/main/main.py`  
    Executa uma simulação básica sem LangChain, criando instâncias de Lead e Assistente e exibindo o histórico de conversas.
  - `python src/main/main_langchain.py`  
    Integra o uso do LangChain para gerenciar a memória de conversa e resumir interações, útil para contextos com longas conversas.

- **Geração de Relatório Diário:**
  - Crie um script (por exemplo, `real_daily_report.py`) que utiliza um fetcher (como `SeleniumConversationsFetcher` ou um fetcher local) para coletar conversas de `assets/chatbase` e gerar o relatório:
    ```python
    from src/reports.daily_report import DailyReport
    from src/reports.fetcher_selenium import SeleniumConversationsFetcher

    fetcher = SeleniumConversationsFetcher(driver_path="path/to/chromedriver", url="https://web.whatsapp.com/")
    report = DailyReport(fetcher=fetcher, model_store="src/reports/model_store.json")
    resultado = report.generate_report()
    print(resultado)
    ```
  - **Treino de Embeddings:**  
    Execute o script `train_model.py` (se disponível) para gerar o dataset a partir de `assets/chatbase`, treinar o classificador multi-classe e salvar o modelo em `model_store.json`:
    ```bash
    python src/reports/train_model.py
    ```

- **Execução de Testes:**
  - **Testes Unitários:**  
    ```bash
    python -m unittest discover -s tests/unit_tests
    ```
  - **Testes de Integração:**  
    ```bash
    python -m unittest discover -s tests/integration_tests
    ```
  - **Testes dos Módulos em `reports/`:**  
    ```bash
    python -m unittest discover -s tests/reports
    ```
  - **Testes Reais (Dados Locais) em `tests/reports/real_tests`:**  
    ```bash
    python -m unittest discover -s tests/reports/real_tests
    ```

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
## Principais Scripts

### Na Pasta `main/`

- **`main.py`**:  
  Execução básica (sem LangChain). Cria instâncias de `Lead` e `Assistente`, simula trocas de mensagens e exibe o histórico final.

- **`main_langchain.py`**:  
  Integração com LangChain. Carrega blocos de prompt, configura `LLMChain` para gerenciar memória de conversa e exemplifica uma conversa com suporte a resumo.

### Na Pasta `reports/`

- **`chat_parser.py`**:  
  Lê arquivos rotulados (success/fail) em `assets/chatbase/` e retorna listas de conversas no formato:
  ```json
  {
    "label": "agendou" | "nao_agendou" | ...,
    "lead_id": "...",
    "mensagens": [
      { "from": "lead" | "assistente", "text": "...", "timestamp": "..." },
      ...
    ]
  }
- **`fetcher_base.py`**:  
  Define a interface `ConversationsFetcher` para a coleta de conversas. As classes concretas (por exemplo, para API ou Selenium) devem implementar essa interface.

- **`fetcher_selenium.py`**:  
  Exemplo de fetcher que utiliza Selenium para captar conversas do dia.

- **`fetcher_api.py`**:  
  Exemplo de fetcher que utiliza endpoints de API para obter conversas.

- **`embeddings_utils.py`**:  
  Carrega um modelo Sentence-BERT e fornece funções para gerar embeddings e calcular similaridade.

- **`embedding_extractor.py`**:  
  Treina um classificador (por exemplo, usando logistic regression) com embeddings gerados das mensagens. Este módulo pode trabalhar com dois rótulos (agendou vs. nao_agendou) ou com múltiplas classes (agendou, cancelou, pendencia, etc.). O classificador é salvo e carregado a partir de um arquivo (por exemplo, `model_store.json`).

- **`synonyms_utils.py`**:  
  Lida com um dicionário de sinônimos (por exemplo, associando "nota" a "nota fiscal") e permite fuzzy matching para enriquecer a compreensão dos termos.

- **`synonyms_extractor.py`**:  
  Autoenriquece a base de sinônimos ao detectar novos tokens não mapeados. Possui o método `integrate_pendentes()`, que, interativamente (ou via heurística), pergunta se determinado token pendente deve ser integrado a um sinônimo existente.

- **`daily_report.py`**:  
  Gera o relatório diário consolidando as conversas coletadas e processadas. Utiliza um `ConversationsFetcher` (Selenium, API ou local), integra o classificador multi-classe (via embeddings) e a base de sinônimos para detectar:
  - Agendamentos realizados
  - Cancelamentos
  - Pendências direcionadas ao médico  
    (Ex.: solicitações de nota fiscal, exame ou receita que não foram resolvidas, a menos que haja uma resposta com termos como “resolvido” ou “enviado”.)

### Outros Scripts (Exemplos)

- **`real_daily_report.py`**:  
  Exemplo de script que carrega um fetcher local (por exemplo, `LocalFileFetcher` que lê dados reais de `assets/chatbase`) e roda o `DailyReport` com dados reais.

- **`train_model.py`**:  
  Script para gerar o dataset a partir dos históricos de conversas, treinar o classificador multi-classe com embeddings e salvar o modelo no arquivo `model_store.json`.

---

## Métricas Principais

### Métricas de Relatório de Conversa:
1. **Agendamentos realizados**  
2. **Cancelamentos**  
3. **Pendências direcionadas ao médico**  
   (Cada métrica é identificada através de análises textuais combinadas com o classificador de embeddings e a base de sinônimos.)

### Métricas de Auditoria Técnica de Conversas (humano ou máquina):
1. **Aptidao para o funil**  
   Avalia a aptidão do lead para o funil, comparando sinais de alta e baixa aptidão.

2. **Temperatura do lead**  
   Determina a "temperatura" do lead, atribuindo uma pontuação (ex.: 10 para alta temperatura, 5 para média, 2 para baixa).

3. **Conversão**  
   Verifica se a conversa indica conversão (interesse em agendamento efetivado).

4. **Respostas genéricas**  
   Calcula a porcentagem de respostas genéricas na interação, sugerindo falta de personalização.

5. **Grau de robotização**  
   Quantifica o nível de automatismo (robotização) das respostas, indicando se há muita repetição ou rigidez no diálogo.

6. **Compreensão semântica**  
   Mede a similaridade semântica entre perguntas e respostas, avaliando se o contexto foi mantido.

7. **Adequação gramatical**  
   Verifica a correção gramatical das respostas, utilizando o LanguageTool para identificar erros.

8. **Fuga das atribuições**  
   Avalia se a assistente respeita suas atribuições, evitando encaminhar questões que não lhe competem.

9. **Conhecimento dos serviços**  
   Analisa se a assistente demonstra conhecimento adequado dos serviços oferecidos.

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

A pasta de **assets** contém os arquivos essenciais para a configuração e execução do framework:

- **assistant_prompt.json**: Contém os blocos (chunks) do prompt da assistente, que são carregados e usados para gerar mensagens com base nas diretrizes de atendimento.
- **sinonimos.json**: Base de sinônimos utilizada para enriquecer a compreensão dos termos. Essa base pode ser atualizada automaticamente via o módulo de extração de sinônimos.
- **chatbase/**: Reúne os históricos de conversas rotuladas, organizados em duas subpastas:
  - **success_cases/**: Contém os logs de conversas de leads que agendaram e compareceram (casos de sucesso).
  - **fail_cases/**: Contém os logs de conversas de leads que não agendaram, cancelaram ou tiveram problemas de comunicação (casos de falha).

Esses arquivos e pastas fornecem o insumo necessário para o treinamento do classificador de embeddings, para o parser de conversas e para a extração de palavras-chave, além de serem fundamentais para a geração dos relatórios diários.

---

## Uso

### Execução Básica (Sem LangChain)

### Execução dos Scripts em `main/`

- **`python src/main/main.py`**: Execução básica, sem LangChain.
- **`python src/main/main_langchain.py`**: Execução com LangChain.

### Scripts Diversos na Pasta `reports/`

- **`python src/reports/train_model.py`** (exemplo): Gera embeddings, treina logistic regression.
- **`python src/reports/real_daily_report.py`** (exemplo): Pega conversas via `LocalFileFetcher`, roda `DailyReport`, imprime relatório.
- **`python src/reports/synonyms_extractor.py`**: Extração de tokens pendentes para sinônimos.

### Geração de Relatório Diário

- Em `src/reports/daily_report.py`, a classe `DailyReport` gera o relatório diário usando um `ConversationsFetcher` (por exemplo, implementado via Selenium, API ou LocalFileFetcher) e o classificador multi-classe treinado, que é carregado a partir do arquivo `model_store.json`.  
- O classificador foi treinado utilizando embeddings gerados por Sentence-BERT, permitindo distinguir rótulos como “agendou”, “cancelou”, “pendencia” e “nao_agendou”. Além disso, o relatório integra uma lógica de detecção refinada para pendências, verificando se mensagens do assistente indicam que a pendência foi resolvida (por exemplo, com termos como “resolvido”, “enviado” ou “emitido”).  
- Para executar, crie um script ou teste, por exemplo:

```python
from src.reports.daily_report import DailyReport
from src.reports.fetcher_selenium import SeleniumConversationsFetcher

# Exemplo utilizando Selenium: forneça o caminho correto para o ChromeDriver e a URL apropriada
fetcher = SeleniumConversationsFetcher(driver_path="path/to/chromedriver", url="https://web.whatsapp.com/")

# Cria o relatório diário, carregando o classificador treinado de 'model_store.json'
report = DailyReport(fetcher=fetcher, model_store="src/reports/model_store.json")
resultado = report.generate_report()
print(resultado)

## Testes

### Testes Unitários

```bash
python -m unittest discover -s tests/unit_tests
```
- Verifica módulos isolados, como analise, agentes, etc.

### Testes de Integração

```bash
python -m unittest discover -s tests/integration_tests
```
- Checa interação global com Selenium ou API.

### Testes na Pasta `reports`

```bash
python -m unittest discover -s tests/reports
```
- Inclui scripts específicos que testam parser, synonyms e daily report.

### Testes Reais (dados locais)

```bash
python -m unittest discover -s tests/reports/real_tests
```
- Usa `LocalFileFetcher` lendo `assets/chatbase` e roda fluxo de embeddings + relatório.

---

## Considerações Adicionais

- **Modelos Leves**  
  Utiliza `EleutherAI/gpt-neo-125M` e `distilgpt2` para execução local. Você pode trocar por modelos mais robustos se tiver recursos de GPU.

- **Gerenciamento de Contexto**  
  LangChain e técnicas de truncamento/sumarização ajudam a manter conversas longas sem exceder os limites de tokens.

- **Prompt da Assistente**  
  Agora fragmentado em blocos JSON, facilitando o uso seletivo ou concatenado, sem arriscar cortes abruptos de contexto.

- **Relatório Diário**  
  Possui arquitetura modular: fetchers diferentes (Selenium, API) e `daily_report.py` para calcular métricas (agendamentos, cancelamentos, pendências).

---

## Licença

Este projeto está licenciado sob a licença [MIT](LICENSE).

---

## Contribuições

Sinta-se à vontade para abrir issues ou enviar pull requests. Toda ajuda é bem-vinda no aprimoramento deste framework!

