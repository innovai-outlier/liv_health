# tests/reports/test_chat_parser.py
import unittest
import os
from src.reports.chat_parser import parse_line, parse_chat_file

class TestChatParser(unittest.TestCase):
    def test_parse_line_ok(self):
        line = "[11/02/2025, 11:46:30] Dra Cristal Endocrinologista: Certo. Qual seu nome?"
        parsed = parse_line(line)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["from"], "assistente")
        self.assertIn("Qual seu nome", parsed["text"])

    def test_parse_line_fail(self):
        line = "This is not a valid line"
        parsed = parse_line(line)
        self.assertIsNone(parsed)

    def test_parse_chat_file(self):
        # Criar um arquivo temporário
        temp_file = "temp_chat.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write("[11/02/2025, 11:46:30] Lead Person: Hello\n")
            f.write("[11/02/2025, 11:47:00] Dra Cristal: Oi\n")

        result = parse_chat_file(temp_file, label="agendou")
        self.assertEqual(result["label"], "agendou")
        self.assertEqual(len(result["mensagens"]), 2)

        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    unittest.main()
