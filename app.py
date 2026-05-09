from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos temporal (en memoria)
productos = [
    {"id": 1, "nombre": "Teclado Mecánico", "precio": 100},
    {"id": 2, "nombre": "Mouse Óptico", "precio": 50}
]

# RUTA GET: Listar productos
@app.route('/productos', methods=['GET'])
def get_productos():
    return jsonify(productos)

# RUTA POST: Agregar un producto
@app.route('/productos', methods=['POST'])
def add_producto():
    nuevo_producto = request.get_json()
    # Validación simple (útil para tus clases de pruebas)
    if not nuevo_producto or 'nombre' not in nuevo_producto:
        return jsonify({"error": "Faltan datos"}), 400
    
    productos.append(nuevo_producto)
    return jsonify(nuevo_producto), 201

if __name__ == '__main__':
    # Importante: host='0.0.0.0' para que Docker permita conexiones externas
    app.run(debug=True, host='0.0.0.0', port=5000)
