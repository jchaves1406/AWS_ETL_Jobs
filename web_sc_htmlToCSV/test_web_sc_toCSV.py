import unittest

from bs4 import BeautifulSoup

from web_sc_htmlToCSV import obtener_bloques


class TestObtenerBloques(unittest.TestCase):

    def setUp(self):
        self.html = """
        <html>
        <head>
                <title>Prueba de obtener_bloques()</title>
        </head>
        <body>
                <div class="item">Bloque 1</div>
                <div class="item">Bloque 2</div>
                <div class="otro-item">No encontrado</div>
        </body>
        </html>
        """
        self.soup = BeautifulSoup(self.html, "html.parser")

    def test_obtener_bloques(self):
        class_item = "item"
        bloques = obtener_bloques(self.soup, class_item)
        self.assertEqual(len(bloques), 2)

        bloque1 = bloques[0]
        bloque2 = bloques[1]
        self.assertEqual(bloque1.text.strip(), "Bloque 1")
        self.assertEqual(bloque2.text.strip(), "Bloque 2")
