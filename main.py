from flask import Flask, request, jsonify, render_template
import mysql.connector
import requests
import json

app = Flask(__name__)

# Configuration de MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': 'escribir clave',  
    'database': 'web_project',
    'port' : '3306'
}

# Funcion para conectar con MySQL
def connect_db():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Endpoint de Llama 3.2
llama_api_url = "http://localhost:11434/api/generate"


# Funcion para renderizar la pagina HTML
@app.route('/')
def index():
    return render_template('index.html')


# SECCION IZQUIERDA

# Funcion para llamar a Llama 3.2
def query_llama(prompt):
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "parameters": {"temperature": 0.0}
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(llama_api_url, json=payload, headers=headers, stream = True)

    full_response = ""  # dejar vacio para unificar toda la respuesta

    for chunk in response.iter_lines():
        if chunk:
            try:
                decoded_chunk = chunk.decode('utf-8')
                json_response = json.loads(decoded_chunk)
                full_response += json_response.get("response", "")  # Extraer y unir 'response' 
            except json.decoder.JSONDecodeError as e:
                print("Failed to decode JSON:", e)

    return full_response


# Funcion para analizar un ID especifico
@app.route('/analyze_recipe', methods=['POST'])
def analyze_recipe():
    recipe_id = request.json.get('recipe_id')
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM 25_recipes WHERE recipe_id = %s", (recipe_id,))
    recipe = cursor.fetchone()
    
    if recipe:
        prompt = f"Por favor analiza la receta con el ID {recipe['recipe_id']} que se llama '{recipe['title']}'. " \
                 f"Los ingredientes son: {recipe['ingredients']}. Los pasos son: {recipe['steps']}. " \
                 f"""Asume que eres un chef Colombiano experto en edicion de texto y estas revisando informacion de recetas para encontrar posibles errores gramaticales o problemas de coherencia para sugerir mejoras. 
                   Revisa si se puede mejorar algo en la redaccion para que sea mas sencillo de entender para una persona que no sea experta en cocinar. Provee todo los comentarios y sugerencias relevantes indicando siempre
                   primero el identificador de la receta, el titulo/nombre y tus comentarios. Especifica a que seccion se refieren cada uno de tus comentarios y sugerencias (titulo, ingredientes, o pasos). 
                   Hazlo todo en una forma estructurada, organizando bien tus comentarios y sugerencias para que sean faciles de seguir por el lector, puedes darle ideas al usuario de qué agregar. Además, 
                   considera agregar separaciones adecuadas en tu respuesta: espacios, punto y aparte, etc. Si es apropiado, dale al usuario un ejemplo de recomendacion de acuerdo a tus comentarios, por jemplo, si le recomiendas
                   modificar el titulo, dale una idea de cómo podría modificarlo, o si le recomiendas modificar la descripción de un ingrediente, dale una idea de cómo escribirlo:"""
        llama_response = query_llama(prompt)
        return jsonify({'llama_response': llama_response})
    else:
        return jsonify({'error': 'Receta no encontrada'})

# Funcion para analizar un rango de IDs
@app.route('/analyze_range', methods=['POST'])
def analyze_range():
    range_start = request.json.get('range_start')
    range_end = request.json.get('range_end')
    
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM 25_recipes WHERE recipe_id BETWEEN %s AND %s", (range_start, range_end))
    recipes = cursor.fetchall()
    
    if recipes:
        prompt = """Por favor analiza las siguientes recetas asumiendo que eres un chef Colombiano experto en edicion de texto y estas revisando informacion de recetas para encontrar posibles errores gramaticales o problemas de coherencia y sugerir mejoras. 
                   Revisa si se puede mejorar algo en la redaccion para que sea mas sencillo de entender para una persona que no sea experta en cocinar. Provee todo los comentarios y sugerencias relevantes indicando siempre
                   primero el identificador de cada receta, el titulo/nombre y tus comentarios, especificando a que seccion se refieren cada uno de tus comentarios (titulo, ingredientes, o pasos). 
                   Hazlo todo en una forma estructurada, organizando bien tus comentarios y sugerencias para que sean faciles de seguir por el lector, así que considera agregar
                    separaciones adecuadas en el contenido de tu respuesta"""
        for recipe in recipes:
            prompt += f"\nReceta ID {recipe['recipe_id']}, Título: '{recipe['title']}', Ingredientes: {recipe['ingredients']}, Pasos: {recipe['steps']}."
        
        llama_response = query_llama(prompt)
        return jsonify({'llama_response': llama_response})
    else:
        return jsonify({'error': 'No se encontraron recetas en ese rango'})

# Funcion para analizar texto libre (Interacción con Llama)
@app.route('/analizar', methods=['POST'])
def analizar_receta():
    data = request.get_json()
    recipe_text = data.get("text", "")

    if not recipe_text:
        return jsonify({"result": "Por favor, ingresa texto para analizar."}), 400

    prompt = f"""Por favor, analiza el siguiente texto de receta de cocina asumiendo que eres un chef Colombiano experto en edicion de texto y estas revisando informacion de recetas para encontrar posibles errores gramaticales o problemas de coherencia 
                    para sugerir mejoras. Revisa si se puede mejorar algo en la redaccion para que sea mas sencillo de entender para una persona que no sea experta en cocinar. Provee todo tus comentarios y sugerencias relevantes indicando siempre
                   primero el identificador de cada receta, el titulo/nombre y tus comentarios, especificando a que seccion se refieren cada uno de tus comentarios (titulo, ingredientes, o pasos). 
                   Hazlo todo en una forma estructurada, organizando bien tus comentarios y sugerencias para que sean faciles de seguir por el lector, así que considera agregar
                    separaciones adecuadas en el contenido de tu respuesta:\n{recipe_text}"""
    llama_response = query_llama(prompt)

    return jsonify({"result": llama_response}), 200


# SECCION-DERECHA

# Buscar receta
@app.route('/search_recipe', methods=['POST'])
def search_recipe():
    recipe_id = request.json['recipe_id']
    print(f"Searching for recipe ID: {recipe_id}")  
    
    # Connectar con base de datos
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Query y enviar resultado
    cursor.execute("SELECT * FROM 25_recipes WHERE recipe_id = %s", (recipe_id,))
    recipe = cursor.fetchone()

    cursor.close()
    connection.close()

    if recipe:
        print(f"Recipe found: {recipe}")  
        return jsonify(recipe)
    else:
        print("Recipe not found")  #
        return jsonify({'error': 'Recipe not found'}), 404


# Funcion para actualizar, borrar o agregar receta
@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    recipe_id = request.json.get('recipe_id')
    title = request.json.get('title')
    ingredients = request.json.get('ingredients')
    steps = request.json.get('steps')
    
    connection = connect_db()
    cursor = connection.cursor()
    
    cursor.execute("UPDATE 25_recipes SET title = %s, ingredients = %s, steps = %s WHERE recipe_id = %s",
                   (title, ingredients, steps, recipe_id))
    connection.commit()
    return jsonify({'success': True})


@app.route('/delete_recipe', methods=['POST'])
def delete_recipe():
    recipe_id = request.json.get('recipe_id')
    
    connection = connect_db()
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM 25_recipes WHERE recipe_id = %s", (recipe_id,))
    connection.commit()
    return jsonify({'success': True})


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    title = request.json.get('title')
    ingredients = request.json.get('ingredients')
    steps = request.json.get('steps')

    connection = connect_db()
    cursor = connection.cursor()

    # Obtener ultimo ID
    cursor.execute("SELECT MAX(recipe_id) FROM 25_recipes")
    last_id = cursor.fetchone()[0]
    new_id = last_id + 1 if last_id else 1

    # Insertar nueva receta con el nuevo ID correspondiente
    cursor.execute("INSERT INTO 25_recipes (recipe_id, title, ingredients, steps) VALUES (%s, %s, %s, %s)",
                   (new_id, title, ingredients, steps))
    connection.commit()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)