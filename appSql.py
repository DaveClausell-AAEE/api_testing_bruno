from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "base_de_datos.db"

# Función para conectar a la base de datos
def conectar_db():
    conn = sqlite3.connect(DB_FILE)
    # Esto nos permite mapear las columnas por su nombre (ej: fila['price'])
    conn.row_factory = sqlite3.Row  
    return conn

# Inicialización: Crea el archivo y la tabla si no existen
def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            stock INTEGER
        )
    """)
    conn.commit()
    conn.close()

# --- RUTAS DE LA API ---

# 1. Obtener todos los productos (GET)
@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    filas = cursor.fetchall()
    conn.close()
    
    # Convertimos cada fila de la DB en un diccionario JSON
    productos = [dict(fila) for fila in filas]
    return jsonify(productos), 200

# 2. Obtener un producto por ID (GET)
@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto_por_id(producto_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    fila = cursor.fetchone()
    conn.close()
    
    # BUG 4: Si no existe el ID, intentará convertirlo a dict y arrojará un Error 500
    # (El código correcto debería validar: if fila is None: return ..., 404)
    return jsonify(dict(fila)), 200

# 3. Crear un nuevo producto (POST)
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    
    # BUG 1, 2 y 3: No hay ninguna validación de datos. 
    # Acepta JSON vacíos, números negativos o textos en el stock.
    name = data.get('name')
    price = data.get('price')
    stock = data.get('stock')
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"id": nuevo_id, "name": name, "price": price, "stock": stock}), 201

# 4. Eliminar un producto (DELETE)
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # BUG 5: Intenta borrar sin verificar si el ID existe en la base de datos.
    # En una API profesional se verifica primero o se controla el rowcount.
    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"mensaje": "Producto eliminado"}), 200

if __name__ == '__main__':
    inicializar_db()  # Llama a la creación de la DB antes de encender la API
    app.run(host='0.0.0.0', port=5000)
