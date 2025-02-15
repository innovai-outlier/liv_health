bot_teste_sdr/
├── agentes.py           # Classes Agent, Lead e Assistente
├── analise.py           # Funções de avaliação das métricas e sinônimos
├── base_conversas.py    # Gerenciamento da base histórica de conversas
├── configuracoes.py     # Configurações gerais, carregamento de modelos e da base de sinônimos
├── constantes.py        # Palavras-chave e expressões (valores "hard-coded")
├── selenium_bot.py      # Automação com Selenium para auditoria dinâmica (suporta URL opcional)
├── sinonimos.py         # Funções para extração e expansão da base de sinônimos
├── main.py              # Script principal para executar auditorias (dinâmica ou estática)
├── sinonimos.json       # Base de sinônimos (gerada e atualizada automaticamente)
├── README.md            # Documentação do projeto
├── LICENSE              # Licença MIT
├── .gitignore           # Arquivo para ignorar arquivos desnecessários no Git
├── requirements.txt     # Dependências do projeto
└── tests/               # Pasta de testes unitários
    ├── __init__.py      # (Arquivo vazio para tratar a pasta como pacote)
    ├── test_analise.py
    ├── test_agentes.py
    ├── test_sinonimos.py
    ├── test_base_conversas.py
    └── test_selenium_bot.py
