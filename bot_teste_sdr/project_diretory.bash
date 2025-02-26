bot_teste_sdr/
├── assets/
│   ├── chatbase/
│   ├── assistente_prompt.json
│   ├── sinonimos.json
├── src/
│   ├── agents/
│   ├── analysis/
│   ├── config/
│   ├── interface/
│   ├── main/
│   ├── reports/
│   │   ├── chat_parser.py
│   │   ├── daily_report.py
│   │   ├── embedding_extractor.py
│   │   ├── embedding_utils.py
│   │   ├── fetcher_api.py
│   │   ├── fetcher_base.py
│   │   ├── fetcher_selenium.py
│   │   ├── keyword_extractor.py
│   │   ├── keyword_utils.py
│   │   ├── synonyms_extractor.py
│   │   ├── synonyms_utils.py
│   │   ├── human_feedback.py  ⬅ **Novo arquivo para captura e aplicação de feedback**
│   │   ├── apply_feedback.py  ⬅ **Novo arquivo para captura e aplicação de feedback**
├── storage/
│   ├── base_conversas.py
├── tests/
│   ├── integration_tests/
│   ├── reports/
│   │   ├── real_tests/
│   │   │   ├── teste_real_daily_report.py
│   │   │   ├── teste_real_chatbase.py
│   │   │   ├── teste_real_embedding.py
│   │   │   ├── teste_real_feedback.py  ⬅ **Novo teste para validar integração do feedback humano**
├── output/
│   ├── relatorio_diario.json  ⬅ **Relatório diário gerado automaticamente**
│   ├── feedback.json  ⬅ **Arquivo onde o feedback é preenchido manualmente**
├── .github/
│   ├── workflows/
│   │   ├── ci.yml  ⬅ **Arquivo atualizado do GitHub Actions para CI/CD**
├── requirements.txt
├── README.md
