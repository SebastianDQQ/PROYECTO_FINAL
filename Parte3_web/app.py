from flask import Flask, render_template, request, url_for
import json
import string

app = Flask(__name__)

with open('datos/revistas_mock.json', encoding='utf-8') as f:
    journals = json.load(f)

def get_unique_areas():
    areas = set()
    for j in journals.values():
        for area in j.get('areas', []):
            areas.add(area)
    return sorted(areas)

def get_unique_catalogos():
    catalogs = set()
    for j in journals.values():
        for catalog in j.get('catalogos', []):
            catalogs.add(catalog)
    return sorted(catalogs)

@app.route('/')
def index():
    return render_template('index.html', journals=journals)

# Ruta que lista las áreas disponibles
@app.route('/area')
def area():
    areas = get_unique_areas()
    return render_template('area.html', areas=areas)

# Al hacer click en un área se muestra la tabla con revistas de esa área
@app.route('/area/<area_name>')
def journals_by_area(area_name):
    filtered = {key: j for key, j in journals.items() if area_name in j.get('areas', [])}
    return render_template('tabla.html', title=f'Revistas en Área: {area_name}', journals=filtered)

# Ruta que lista los catálogos disponibles
@app.route('/catalogo')
def catalogo():
    catalogs = get_unique_catalogos()
    return render_template('catalogo.html', catalogs=catalogs)

# Mostrar con una tabla las revistas que pertenecen a un catálogo seleccionado
@app.route('/catalogo/<catalogo_name>')
def journals_by_catalog(catalogo_name):
    filtered = {key: j for key, j in journals.items() if catalogo_name in j.get('catalogos', [])}
    return render_template('tabla.html', title=f'Revistas en Catálogo: {catalogo_name}', journals=filtered)

# Sección de explorar: se muestra un abecedario
@app.route('/explorar')
def explorar():
    letters = list(string.ascii_uppercase)
    return render_template('explorar.html', letters=letters)

# Al hacer click en una letra del abecedario se filtran las revistas cuyo título inicie con esa letra
@app.route('/explorar/<letter>')
def journals_by_letter(letter):
    filtered = {key: j for key, j in journals.items() if key.upper().startswith(letter.upper())}
    return render_template('explorar.html', selected_letter=letter.upper(), journals=filtered, letters=list(string.ascii_uppercase))

# Ruta de búsqueda: se realiza la búsqueda de palabras en título, áreas o catálogos
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

# Página de detalle de una revista
@app.route('/revista/<journal_id>')
def revista(journal_id):
    journal = journals.get(journal_id)
    if journal:
        return render_template('revista.html', journal_id=journal_id, journal=journal)
    else:
        return "Revista no encontrada", 404

# Página de créditos
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