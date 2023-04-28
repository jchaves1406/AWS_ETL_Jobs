from unittest import mock


@mock.patch('web_sc_html.descargar_pagina')
def test_descargar_pagina(mock_descargar_pagina):
    url = "https://www.google.com"
    page = mock_descargar_pagina(url)
    mock_descargar_pagina.assert_called_once_with(url)
    assert page is not None
