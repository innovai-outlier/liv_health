# src/interface/selenium_bot.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def iniciar_selenium(url="https://web.whatsapp.com/"):
    options = Options()
    options.add_argument("--user-data-dir=./chrome-data")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    if "dummy" in url:
        options.add_argument("--headless")
    service = Service("C://Users//dmene//OneDrive//INNOVAI//Projetos//LivHealth//ASSISTENTE_VIRTUAL//liv_health//bot_teste_sdr//chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
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
