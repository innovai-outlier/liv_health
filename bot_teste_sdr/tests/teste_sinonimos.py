import unittest
from sinonimos import encontrar_sinonimos, expandir_sinonimos
from configuracoes import DICIONARIO_SINONIMOS

class TestSinonimos(unittest.TestCase):
    def test_encontrar_sinonimos(self):
        sinonimos = encontrar_sinonimos("agendar")
        self.assertIsInstance(sinonimos, set)
        self.assertTrue("marcar" in sinonimos or "reservar" in sinonimos)

    def test_expandir_sinonimos(self):
        initial_count = len(DICIONARIO_SINONIMOS.get("consulta", []))
        expandir_sinonimos(["consulta"])
        new_count = len(DICIONARIO_SINONIMOS.get("consulta", []))
        self.assertGreaterEqual(new_count, initial_count)

if __name__ == "__main__":
    unittest.main()
