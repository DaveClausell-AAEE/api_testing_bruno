from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = "base_de_datos.db"

def conectar_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  
    return conn

def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- MIDDLEWARE DE VALIDACIÓN Y SANITIZACIÓN ---
def validar_payload_producto(data):
    if not data or not isinstance(data, dict):
        return "El cuerpo de la petición debe ser un objeto JSON válido."

    # BUG-01: Validación de Campos Obligatorios
    campos_requeridos = ['nombre', 'precio', 'stock']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None:
            return f"Falta el campo obligatorio requerido: '{campo}'."

    nombre = data.get('nombre')
    precio = data.get('precio')
    stock = data.get('stock')

    # BUG-03 / BUG-06: Consistencia estricta de tipos de datos
    if not isinstance(nombre, str):
        return "El campo 'nombre' debe ser una cadena de texto (string)."
    
    # Python puede recibir un entero y guardarlo como float de forma segura
    if not isinstance(precio, (int, float)) or isinstance(precio, bool):
        return "El campo 'precio' debe ser un valor numérico (float o int)."
        
    # Evitamos que pasen booleanos (True/False) que en Python heredan de int
    if not isinstance(stock, int) or isinstance(stock, bool):
        return "El campo 'stock' debe ser estrictamente un número entero (int)."

    # BUG-06: Sanitización de longitud del campo nombre
    nombre_limpio = nombre.strip()
    if len(nombre_limpio) == 0:
        return "El campo 'nombre' no puede estar vacío ni contener solo espacios."
    if len(nombre_limpio) > 80:
        return "El campo 'nombre' excede el límite máximo permitido de 80 caracteres."

    # BUG-06: Sanitización básica contra XSS e inyecciones de etiquetas HTML
    if "<script>" in nombre_limpio or "</script>" in nombre_limpio:
        return "El campo 'nombre' contiene caracteres o etiquetas no permitidas."

    # BUG-02: Validación de Rangos Financieros y Logísticos (Límites)
    if precio <= 0:
        return "El campo 'precio' debe ser un número positivo mayor a 0."
    if stock < 0:
        return "El campo 'stock' no puede ser un número negativo."

    return None

# --- RUTAS DE LA API (ENDPOINT BLINDADO) ---

# 1. Obtener todos los productos (GET) - Blindado ante SQLI
@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = conectar_db()
    cursor = conn.cursor()
    # Las consultas directas sin concatenación de strings mitigan el ataque de inyección SQL (BUG-06)
    cursor.execute("SELECT id, name, price, stock FROM productos")
    filas = cursor.fetchall()
    conn.close()
    
    # Estructuramos la respuesta mapeando las claves en español para consistencia externa
    productos = [
        {"id": fila['id'], "nombre": fila['name'], "precio": fila['price'], "stock": fila['stock']} 
        for fila in filas
    ]
    return jsonify(productos), 200

# 2. Obtener un producto por ID (GET individual) - Control de Error 500 (BUG-04)
@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto_por_id(producto_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, stock FROM productos WHERE id = ?", (producto_id,))
    fila = cursor.fetchone()
    conn.close()
    
    # Manejo de Excepciones: Si no existe el recurso en DB, responde 404 de manera elegante
    if fila is None:
        return jsonify({"error": f"Producto con ID {producto_id} no encontrado"}), 404
        
    producto = {"id": fila['id'], "nombre": fila['name'], "precio": fila['price'], "stock": fila['stock']}
    return jsonify(producto), 200

# 3. Crear un nuevo producto (POST) - Aplicación de Capa Transversal de Control
@app.route('/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Payload malformado. No se pudo parsear el JSON."}), 400

    # Ejecutamos las validaciones e interrupciones antes de interactuar con la persistencia
    error_validacion = validar_payload_producto(data)
    if error_validacion:
        return jsonify({"error": error_validacion}), 400

    nombre = data.get('nombre').strip()
    precio = float(data.get('precio'))
    stock = int(data.get('stock'))
    
    conn = conectar_db()
    cursor = conn.cursor()
    # Parámetros estrictos que previenen inyección SQL estructural
    cursor.execute(
        "INSERT INTO productos (name, price, stock) VALUES (?, ?, ?)",
        (nombre, precio, stock)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"id": nuevo_id, "nombre": nombre, "precio": precio, "stock": stock}), 201

# 4. Eliminar un producto (DELETE) - Control de Error 500 (BUG-05)
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificación previa de existencia para garantizar la robustez del backend
    cursor.execute("SELECT id FROM productos WHERE id = ?", (producto_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({"error": f"No se puede eliminar: El producto con ID {producto_id} no existe."}), 404
        
    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"mensaje": f"Producto con ID {producto_id} eliminado correctamente."}), 200

if __name__ == '__main__':
    inicializar_db()
    # Mantenemos el puerto 5000 para compatibilidad directa con el contenedor de Docker Desktop
    app.run(host='0.0.0.0', port=5000)
