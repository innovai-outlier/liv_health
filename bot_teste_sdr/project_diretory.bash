📂 Estrutura do Framework de Relatórios e Auditoria

bot_teste_sdr/
├── assets/                  # Base RAW de conversas brutas (antes do parser)
│   ├── chatbase/
│   │   ├── success_cases/
│   │   ├── fail_cases/
│   ├── assistant_prompt.json
│   ├── sinonimos.json
│   └── keywords.json
│
├── database/                # Base formatada para Treino, Teste e Validação
│   ├── train/
│   │   ├── conversations.json
│   ├── test/
│   │   ├── conversations.json
│   ├── validate/
│   │   ├── conversations.json
│
├── benchmark/               # Comparação entre embeddings e IA Generativa
│   ├── benchmark_report.py
│   ├── results/
│   │   ├── benchmark_results.json
│   │   ├── embeddings_report.json
│   │   ├── generative_report.json
│
├── output/                  # Armazena modelos treinados e relatórios
│   ├── model_store.json
│   ├── daily_report.json
│   ├── validation_report.json
│   ├── generative_daily_report.json
│   ├── feedback.json
│
├── src/                     # Código-fonte do Framework
│   ├── reports/             # Módulos para Processamento e Relatórios
│   │   ├── chat_parser.py
│   │   ├── split_chatbase.py
│   │   ├── daily_report.py
│   │   ├── embedding_extractor.py
│   │   ├── generative_model.py
│   │   ├── apply_feedback.py
│   │   ├── fetcher_base.py
│   │   ├── fetcher_selenium.py
│   │   ├── fetcher_api.py
│   │   ├── synonyms_extractor.py
│   │   ├── workflow_reports.py
│   ├── analysis/            # Módulos de auditoria e métricas
│   │   ├── analise.py
│   │   ├── sinonimos.py
│   ├── storage/             # Gerenciamento e persistência de dados
│   │   ├── base_conversas.py
│   ├── interface/           # Interação com WhatsApp (Selenium, API)
│   │   ├── selenium_bot.py
│   ├── main/                # Executáveis principais
│   │   ├── main.py
│   │   ├── main_langchain.py
│   │   ├── main_report_workflow.py
│
├── tests/                   # Testes Automatizados
│   ├── unit_tests/
│   │   ├── test_analise.py
│   │   ├── test_agentes.py
│   ├── integration_tests/
│   │   ├── test_selenium_bot.py
│   │   ├── test_integration_local.py
│   ├── reports/             # Testes dos relatórios e embedding
│   │   ├── real_tests/
│   │   │   ├── test_real_daily_report.py
│   │   │   ├── test_real_embedding.py
│   │   │   ├── test_real_feedback.py
│   │   ├── test_chat_parser.py
│   │   ├── test_keyword_extractor.py
│
├── .github/                  # Configurações do GitHub Actions (CI/CD)
│   ├── workflows/
│   │   ├── ci_cd_pipeline.yml
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
