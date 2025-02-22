project_root/
├── assets/
│   ├── assistente_prompt.txt       # Arquivo com o prompt completo da assistente (texto longo)
│   └── sinonimos.json              # Base de sinônimos (gerada/atualizada automaticamente)
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── configuracoes.py        # Configurações gerais (base de sinônimos, etc.)
│   │   ├── constantes.py           # Listas de expressões e parâmetros (como FUZZY_THRESHOLD)
│   │   └── papis_config.py         # Carregamento dos modelos leves, prompts (carregados de arquivo e resumidos) e parâmetros de geração
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agentes.py              # Classes Agent, Lead e Assistente com métodos de geração
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── analise.py              # Funções de avaliação das métricas
│   │   └── sinonimos.py            # Funções para extração e expansão da base de sinônimos
│   ├── storage/
│   │   ├── __init__.py
│   │   └── base_conversas.py       # Gerenciamento e armazenamento da base histórica de conversas
│   ├── interface/
│   │   ├── __init__.py
│   │   └── selenium_bot.py         # Funções de automação com Selenium
│   └── main/
│       ├── __init__.py
│       ├── main.py                 # Script principal para execução básica (sem LangChain)
│       └── main_langchain.py       # Exemplo de integração com LangChain
├── tests/
│   ├── unit_tests/
│   │   ├── __init__.py
│   │   ├── test_analise.py
│   │   ├── test_agentes.py
│   │   ├── test_sinonimos.py
│   │   └── test_base_conversas.py
│   └── integration_tests/
│       ├── __init__.py
│       ├── test_selenium_bot.py
│       ├── test_integration_local.py
│       └── test_langchain_integration.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
