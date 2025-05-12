from flask import Flask, render_template, request, url_for
import json
import string

app = Flask(__name__)
with open('datos/json/revistas_informacion.json', encoding='utf-8') as f:
    journals = json.load(f)
    
with open('datos/json/revistas.json', encoding='utf-8') as f:
    rev_catalogos = json.load(f)

for journal_key, journal_data in journals.items():
    normalized_key = journal_key.strip().lower()
    if normalized_key in rev_catalogos:
        journal_data["catalogos"] = rev_catalogos[normalized_key].get("catalogos", [])
    else:

        journal_data["catalogos"] = []

for journal in journals.values():
    journal.setdefault("subjet_area_and_category", {}) 
    journal.setdefault("h_index", "No disponible")

def get_unique_areas():
    areas = set()
    for j in journals.values():
        if j.get("subjet_area_and_category"):
            for subject in j["subjet_area_and_category"].keys():
                areas.add(subject)
    return sorted(areas)

def get_unique_catalogos():
    catalogs = set()
    for j in journals.values():
        for catalog in j.get("catalogos", []):
            catalogs.add(catalog)
    return sorted(catalogs)

@app.route('/')
def index():
    return render_template('index.html', journals=journals)

@app.route('/area')
def area():
    areas = get_unique_areas()
    if not areas:
        return "No hay áreas disponibles", 404  
    return render_template('area.html', areas=areas)

@app.route('/area/<area_name>')
def journals_by_area(area_name):
    filtered = {
        key: j for key, j in journals.items() 
        if j.get("subjet_area_and_category") and area_name in j.get("subjet_area_and_category", {})
    }
    if not filtered:
        return "No se encontraron revistas en esta área", 404
    return render_template('tabla_explorar.html', title=f'Revistas en Área: {area_name}', journals=filtered)

@app.route('/catalogo')
def catalogo():
    catalogs = get_unique_catalogos()
    return render_template('catalogo.html', catalogs=catalogs)

@app.route('/catalogo/<catalogo_name>')
def journals_by_catalog(catalogo_name):
    filtered = {key: j for key, j in journals.items() if catalogo_name in j.get("catalogos", [])}
    return render_template('tabla_explorar.html', title=f'Revistas en Catálogo: {catalogo_name}', journals=filtered)

@app.route('/explorar')
def explorar():
    letters = list(string.ascii_uppercase)
    return render_template('explorar.html', letters=letters)

@app.route('/explorar/<letter>')
def journals_by_letter(letter):
    filtered = {key: j for key, j in journals.items() if key.upper().startswith(letter.upper())}
    return render_template('explorar.html', selected_letter=letter.upper(), journals=filtered, letters=list(string.ascii_uppercase))

@app.route('/busqueda', methods=['GET'])
def busqueda():
    query = request.args.get('q', '')
    results = {}
    if query:
        term = query.lower()
        for key, j in journals.items():
            if (term in key.lower() or 
                any(term in area.lower() for area in j.get('areas', [])) or 
                any(term in catalog.lower() for catalog in j.get('catalogos', []))):
                results[key] = j
    return render_template('busqueda.html', results=results, query=query, journals=journals)

@app.route('/revista/<journal_id>')
def revista(journal_id):
    journal = journals.get(journal_id)
    if not journal:
        return "Revista no encontrada", 404  
    journal.setdefault("subjet_area_and_category", {})
    return render_template('revista.html', journal_id=journal_id, journal=journal)

@app.route('/creditos')
def creditos():
    developers = [
        {'nombre': 'Sebastián Duarte Quijada'},
        {'nombre': 'Edgar Arteaga Flores'},
        {'nombre': 'Alan Fernando Ruiz Gracia'}
    ]
    return render_template('creditos.html', developers=developers)

if __name__ == '__main__':
    app.run(debug=True)