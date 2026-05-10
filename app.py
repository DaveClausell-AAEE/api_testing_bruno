from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos ficticia en memoria para la práctica de la clase
productos = [
    {"id": 1, "nombre": "Teclado", "precio": 1500, "stock": 10},
    {"id": 2, "nombre": "Mouse", "precio": 800, "stock": 25}
]

@app.route('/productos', methods=['GET'])
def obtener_productos():
    """Retorna la lista de todos los productos disponibles."""
    return jsonify(productos), 200

@app.route('/productos', methods=['POST'])
def crear_producto():
    """Crea un nuevo producto en el sistema."""
    nuevo_producto = request.get_json()
    
    # --- BUGS INTENCIONALES PARA LA CLASE ---
    # 🕵️ BUG 1: No valida campos obligatorios (nombre, precio, stock).
    # 🕵️ BUG 2: No valida que el precio sea un número positivo.
    # 🕵️ BUG 3: No valida que el stock sea un número entero (permite recibir texto).
    
    nuevo_producto['id'] = len(productos) + 1
    productos.append(nuevo_producto)
    
    return jsonify(nuevo_producto), 201

@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    """Busca un producto específico por su ID numérico."""
    try:
        # 🕵️ BUG 4: Si el ID no existe, el acceso al índice [0] fallará.
        # Esto devolverá un Error 500 (HTML) en lugar de un Error 404 (JSON).
        producto = [p for p in productos if p['id'] == id][0]
        return jsonify(producto), 200
    except Exception:
        # Forzamos una excepción genérica para que el alumno vea el error de servidor
        raise Exception("Fallo crítico en la base de datos al buscar ID")

@app.route('/productos/<int:id>', methods=['DELETE'])
def borrar_producto(id):
    """Elimina un producto del sistema por su ID."""
    global productos
    
    try:
        # 🕵️ BUG 5: Al igual que en el GET, si el ID no existe en la lista,
        # la búsqueda fallará y el servidor colapsará con Error 500.
        producto_a_borrar = [p for p in productos if p['id'] == id][0]
        
        # Filtramos la lista para quitar el producto
        productos = [p for p in productos if p['id'] != id]
        
        return jsonify({"mensaje": f"Producto {id} eliminado exitosamente"}), 200
    except Exception:
        # El servidor falla al no encontrar el recurso, devolviendo Error 500
        return "Internal Server Error", 500

if __name__ == '__main__':
    # Usamos host 0.0.0.0 para que el contenedor Docker sea accesible desde Windows
    app.run(host='0.0.0.0', port=5000, debug=True)
