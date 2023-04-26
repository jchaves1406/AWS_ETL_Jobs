from bs4 import BeautifulSoup
from web_sc_htmlToCSV import obtener_bloques

def test_obtener_bloques():
    # HTML de ejemplo
    html = '''<div class="listing-card__information">Bloque 1</div>
            <div class="listing-card__information">Bloque 2</div>'''
    soup = BeautifulSoup(html, 'html.parser')

    # Obtener los bloques de información con la función
    bloques = obtener_bloques(soup)

    # Verificar que se obtuvieron los bloques correctos
    assert len(bloques) == 2
    assert bloques[0].text == "Bloque 1"
    assert bloques[1].text == "Bloque 2"