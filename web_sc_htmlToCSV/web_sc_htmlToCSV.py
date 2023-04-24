import sys
import pandas as pd
import boto3
import datetime
import io
from bs4 import BeautifulSoup


s3 = boto3.client('s3')
date = datetime.date.today()
bucket_name = 'bucket-raw-html'


# Función que se encarga de recibir la url de un html
# y devuelve un parseo con el contenido del documento
def leer_pagina(url):
    return BeautifulSoup(url, "html.parser")


def obtener_bloques_publimetro(page):
    return page.find_all("div", attrs={"class": "list-item"})


def obtener_bloques_eltiempo(page):
    return page.find_all("div", attrs={"class": "listing"})


def extraer_atributos_publimetro(bloques):
    noticias = []
    # Iterar sobre cada bloque y obtener la información relevante
    for bloque in bloques:
        categoria = str(bloque.find('a')['href']).split('/')[1].capitalize()
        titulo = bloque.find(
            'h2', {'class': 'primary-font__PrimaryFontStyles-o56yd5-0 ctbcAa headline-text'}).text.strip()
        link = 'https://www.publimetro.co' + bloque.find('a')['href']

        # Crear un diccionario con los atributos extraídos
        noticia = {"categoria": categoria, "titulo": titulo, "enlace": link}
        noticias.append(noticia)
    # Crear un DataFrame a partir de la lista de noticias
    df = pd.DataFrame(noticias, columns=noticia.keys())
    df = df.drop_duplicates()
    return df


def extraer_atributos_eltiempo(bloques):
    noticias = []
    # Iterar sobre cada bloque y obtener la información relevante
    for i in range(1, len(bloques)):
        categoria = bloques[i].find(
            'div', {'class': 'category'}).text.strip()
        titulo = bloques[i].find(
            'a', {'class': 'title page-link'}).text.strip()
        link = 'https://www.eltiempo.com' + bloques[i].find(
            'a', {'class': 'title page-link'}).get('href')

        # Crear un diccionario con los atributos extraídos
        noticia = {"categoria": categoria, "titulo": titulo, "enlace": link}
        noticias.append(noticia)
    # Crear un DataFrame a partir de la lista de noticias
    df = pd.DataFrame(noticias, columns=noticia.keys())
    df = df.drop_duplicates()
    return df
    

def obtener_contenido():
    file_name = 'contenido-' + str(date) + '.html'
    key = f'headlines/raw/{file_name}'
    response = s3.get_object(Bucket=bucket_name, Key=key)
    contenido = response['Body'].read()
    return contenido


def guardar_contenido(df, periodico):
    file_csv_eltiempo = 'contenido-' + str(date) + '.csv'
    key = f'headlines/final/periodico={periodico}/year={date.year}/month={date.month}/day={date.day}/{file_csv_eltiempo}'
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, sep=';', header=False)
    csv_buffer.seek(0)
    # Sube el archivo a S3
    s3.put_object(Bucket=bucket_name, Key=key,
                  Body=csv_buffer.getvalue())


contenido = obtener_contenido()
page = leer_pagina(contenido)
bloques_eltiempo = obtener_bloques_eltiempo(page)
df_eltiempo = extraer_atributos_eltiempo(bloques_eltiempo)
bloques_publimetro = obtener_bloques_publimetro(page)
df_publimetro = extraer_atributos_publimetro(bloques_publimetro)
guardar_contenido(df_eltiempo, 'eltiempo')
guardar_contenido(df_publimetro, 'publimetro')
