import sys
import boto3
import requests
from datetime import datetime


s3 = boto3.client('s3')


# Función que descarga el contenido de una página web y lo
# retorna como un string.
def descargar_pagina(url):
    return requests.get(url).text


# Función que recorre varias páginas de búsqueda de noticias
# de El Tiempo y retorna el contenido.
def cantidad_paginas_eltiempo(paginas):
    contenido = ''
    for i in range(1, paginas):
        url = f'https://www.eltiempo.com/buscar/{i}?q=noticias'
        contenido += descargar_pagina(url)
    return contenido


# Función que genera el contenido de noticias a partir de
# dos fuentes distintas.
def generar_contenido_noticias():
    contenido = ''
    url = 'https://www.publimetro.co/noticias/'
    contenido += descargar_pagina(url)
    contenido += cantidad_paginas_eltiempo(4)
    return contenido


# Generación del contenido de noticias.
contenido = generar_contenido_noticias()

# Se sube el archivo generado al bucket 'bucket-raw-html' de
# S3, en la carpeta 'headlines/raw'.
bucket_name = 'bucket-raw-html'
file_name = 'contenido-' + datetime.utcnow().strftime('%Y-%m-%d') + '.html'
s3.put_object(Bucket=bucket_name, Key=f'headlines/raw/{file_name}',
              Body=contenido, ContentType='text/html')
