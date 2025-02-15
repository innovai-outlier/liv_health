# selenium_bot.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def iniciar_selenium(url="https://web.whatsapp.com/"):
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./chrome-data")
    # Ativa o modo headless para testes automatizados (opcional para testes)
    if "dummy" in url:
        options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    # Se estiver usando a URL padrão do WhatsApp, aguarda o QR Code
    if url == "https://web.whatsapp.com/":
        input("Escaneie o QR Code e pressione ENTER para continuar...")
    return driver

def enviar_mensagem(driver, mensagem):
    input_box = driver.find_element(By.XPATH, '//div[@title="Digite uma mensagem"]')
    input_box.send_keys(mensagem)
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

def capturar_resposta(driver):
    time.sleep(1)
    mensagens = driver.find_elements(By.XPATH, '//div[contains(@class, "message-out")]//span[@class]')
    return mensagens[-1].text if mensagens else None
