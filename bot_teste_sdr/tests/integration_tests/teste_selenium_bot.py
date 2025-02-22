# unit_tests/test_selenium_bot.py
import unittest
import os
import tempfile
from src.interface.selenium_bot import iniciar_selenium, enviar_mensagem, capturar_resposta
from selenium.webdriver.common.by import By

DUMMY_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Dummy WhatsApp</title>
</head>
<body>
    <div title="Digite uma mensagem" contenteditable="true"></div>
    <div class="message-out">
        <span class="dummy">Test Message</span>
    </div>
</body>
</html>
"""

class TestSeleniumBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.gettempdir()
        cls.dummy_file_path = os.path.join(cls.temp_dir, "dummy_whatsapp.html")
        with open(cls.dummy_file_path, "w", encoding="utf-8") as f:
            f.write(DUMMY_HTML)
        cls.dummy_url = "file://" + cls.dummy_file_path

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.dummy_file_path)

    def setUp(self):
        self.driver = iniciar_selenium(url=self.dummy_url)

    def tearDown(self):
        self.driver.quit()

    def test_iniciar_selenium_loads_dummy_page(self):
        title = self.driver.title
        self.assertEqual(title, "Dummy WhatsApp")

    def test_enviar_mensagem(self):
        input_box = self.driver.find_element(By.XPATH, '//div[@title="Digite uma mensagem"]')
        enviar_mensagem(self.driver, "Hello World")
        content = input_box.get_attribute("innerText")
        self.assertIn("Hello World", content)

    def test_capturar_resposta(self):
        resposta = capturar_resposta(self.driver)
        self.assertEqual(resposta, "Test Message")

if __name__ == "__main__":
    unittest.main()
