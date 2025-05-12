import os
import json
import time
import requests
from bs4 import BeautifulSoup

HEADERS_CONFIG = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

BASE_URL = 'https://www.scimagojr.com'
SEARCH_ENDPOINT = BASE_URL + '/journalsearch.php?q='
INPUT_FILE = 'datos/json/revistas.json'
OUTPUT_FILE = 'datos/json/revistas_informacion.json'
LIMIT_REVISTAS = 50000  

revistas_info = {}
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        revistas_info = json.load(f)

def obtener_html(url):
    try:
        resp = requests.get(url, headers=HEADERS_CONFIG, timeout=15)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as err:
        print(f"Error en {url}: {err}")
        return None

def buscar_url_revista(nombre_revista):
    consulta_url = SEARCH_ENDPOINT + nombre_revista.replace(' ', '+')
    html_data = obtener_html(consulta_url)
    if not html_data:
        return None
    
    sopa = BeautifulSoup(html_data, 'html.parser')
    resultado = sopa.select_one('span.jrnlname')
    
    return BASE_URL + '/' + resultado.find_parent('a')['href'] if resultado else None

def obtener_imagen(sopa):
    img_elemento = sopa.find('img', class_='imgwidget')
    return BASE_URL + '/' + img_elemento['src'] if img_elemento and 'src' in img_elemento.attrs else None

def obtener_categoria(sopa):
    seccion = sopa.find("h2", string="Subject Area and Category")
    if not seccion:
        return None
    tabla = seccion.find_next("table")
    if not tabla:
        return None
    return ', '.join(td.get_text(strip=True) for td in tabla.find_all("td") if td)

def extraer_datos_revista(url):
    contenido_html = obtener_html(url)
    if not contenido_html:
        return {}

    sopa = BeautifulSoup(contenido_html, 'html.parser')

    def obtener_texto(seccion_nombre):
        elemento = sopa.find('h2', string=lambda s: s and seccion_nombre in s)
        return elemento.find_next_sibling('p').text.strip() if elemento else None

    return {
        "sitio_web": obtener_texto("Homepage"),
        "indice_h": obtener_texto("H-Index"),
        "categoria_tematica": obtener_categoria(sopa),
        "editorial": obtener_texto("Publisher"),
        "codigo_issn": obtener_texto("ISSN"),
        "imagen_widget": obtener_imagen(sopa),
        "tipo_publicacion": obtener_texto("Publication type"),
        "fuente": url
    }

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    revistas_entrada = json.load(f)

contador = 0
for revista in revistas_entrada:
    if revista in revistas_info:
        print(f"✓ Ya existe: {revista}")
        continue

    if contador >= LIMIT_REVISTAS:
        print(f"Se alcanzó el límite de {LIMIT_REVISTAS}.")
        break

    print(f"→ Buscando: {revista}")
    try:
        url_revista = buscar_url_revista(revista)
        if not url_revista:
            print(f"✗ No se encontró un URL para {revista}")
            continue

        revistas_info[revista] = extraer_datos_revista(url_revista)
        print(f"✓ Datos obtenidos para {revista}")
        contador += 1
        time.sleep(2)
    except Exception as err:
        print(f"✗ Error con {revista}: {err}")

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(revistas_info, f, indent=4, ensure_ascii=False)

print(f"Proceso finalizado. Revistas procesadas: {contador}")