import os
import csv
import json
import re
import unicodedata

def normalize_name(name):
    name = name.strip().lower()

    name = unicodedata.normalize('NFKD', name)
    name = "".join(c for c in name if not unicodedata.combining(c))

    name = re.sub(r'\s+', ' ', name)
    return name

def extraer_etiqueta(filename):
    base = os.path.splitext(filename)[0] 
    if "_RadGridExport" in base:
        etiqueta = base.split("_RadGridExport")[0].strip()
    elif " RadGridExport" in base:
        etiqueta = base.split(" RadGridExport")[0].strip()
    else:
        etiqueta = base.strip()
    return etiqueta

areas_folder = os.path.join("datos", "csv", "areas")
catalogos_folder = os.path.join("datos", "csv", "catalogos")
output_json_path = os.path.join("datos", "json", "revistas.json")
revistas = {}

def procesar_csv_folder(folder, tipo):
    for filename in os.listdir(folder):
        if filename.lower().endswith(".csv"):
            ruta = os.path.join(folder, filename)
            etiqueta = extraer_etiqueta(filename)
            try:
                with open(ruta, mode="r", encoding="utf-8", newline='') as archivo:
                    lector = csv.reader(archivo)
                    for row in lector:
                        if not row:
                            continue
                        journal_raw = row[0]
                        journal = normalize_name(journal_raw)
                        if not journal:
                            continue

                        if journal not in revistas:
                            revistas[journal] = {"areas": [], "catalogos": []}
                        if etiqueta not in revistas[journal][tipo]:
                            revistas[journal][tipo].append(etiqueta)
            except Exception as e:
                print(f"Error al procesar el archivo {ruta}: {e}")

procesar_csv_folder(areas_folder, "areas")
procesar_csv_folder(catalogos_folder, "catalogos")

with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(revistas, f, ensure_ascii=False, indent=4)

print(f"Archivo JSON generado en: {output_json_path}")
