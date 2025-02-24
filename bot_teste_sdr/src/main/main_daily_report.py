# Exemplo: main_daily_report.py (ou algo assim)
from src.report.daily_report import DailyReport
from src.report.fetcher_selenium import SeleniumConversationsFetcher
# ou
# from src.report.fetcher_api import APIConversationsFetcher

def main():
    # Exemplo Selenium:
    selenium_fetcher = SeleniumConversationsFetcher(
        driver_path="path/do/chromedriver",
        url="https://web.whatsapp.com/"
    )
    # Cria o DailyReport usando esse fetcher
    relatorio = DailyReport(fetcher=selenium_fetcher)
    resultado = relatorio.generate_report()

    # Printar ou salvar
    print(resultado)

if __name__ == "__main__":
    main()
