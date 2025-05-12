# Biblioteca de Revistas

Este proyecto tiene como objetivo desarrollar una herramienta que permita explorar información relevante sobre revistas académicas mediante el procesamiento de archivos CSV, técnicas de web scraping y una interfaz web interactiva construida con Flask y Bootstrap.

El sistema está dividido en tres etapas:

1. **Generación de archivo JSON a partir de archivos CSV.**
2. **Obtención automatizada de información desde el sitio web SCImago Journal & Country Rank (https://www.scimagojr.com).**
3. **Visualización de los datos a través de una interfaz web.**

---

## Instrucciones para ejecutar el programa

1. **Ejecutar el archivo `Parte 1_Generar json.py`**  
   Este archivo se encarga de leer los archivos CSV ubicados en los directorios `áreas` y `catálogos`, procesar los datos y generar un archivo JSON denominado `revistas.json`. Este archivo contendrá un diccionario donde cada entrada representa una revista con sus áreas y catálogos asociados.

2. **Ejecutar el archivo `Parte 2_scrap.py`**  
   Este script toma como entrada el archivo `revistas.json` y realiza una búsqueda en el sitio [scimagojr.com](https://www.scimagojr.com) para recopilar información detallada de cada revista. Los datos recuperados incluyen H-Index, sitio web, ISSN, editorial, tipo de publicación, categoría temática, y un widget de SCImago. La salida del script es un nuevo archivo llamado `revistas_informacion.json`.

3. **Ejecutar el archivo `app.py` ubicado en el directorio `Parte 3_web`**  
   Este archivo inicia una aplicación web desarrollada con Flask, la cual lee el archivo `revistas_informacion.json` y muestra los datos de forma estructurada. El sitio permite explorar las revistas por catálogo, por área temática o realizar búsquedas por título. La interfaz incluye los colores institucionales de la Universidad de Sonora, así como su logotipo.

---

## Requisitos del sistema

- Python 3.10 o superior
- Flask
- Requests
- BeautifulSoup4


---

## Integrantes del equipo

- Sebastián Duarte Quijada  
- Edgar Arteaga Flores  
- Alan Fernando Ruiz Gracia  

---

## Asistencia Digital Utilizada

Durante el desarrollo del presente proyecto se utilizó **GitHub Copilot** como asistente de codificación. Esta herramienta fue empleada para generar fragmentos de código, sugerencias en estructuras de control y funciones auxiliares. Todas las decisiones de diseño, lógica de programación y validaciones fueron realizadas por los integrantes del equipo.

---

