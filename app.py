from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos en memoria
productos = [
    {"id": 1, "nombre": "Teclado", "precio": 1500, "stock": 10},
    {"id": 2, "nombre": "Mouse", "precio": 800, "stock": 25}
]

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos), 200

@app.route('/productos', methods=['POST'])
def crear_producto():
    nuevo_producto = request.get_json()
    
    # BUG OCULTO 1: No se valida si faltan campos obligatorios (nombre/precio)
    # BUG OCULTO 2: No se valida que el precio sea un número positivo
    # BUG OCULTO 3: No se valida que el stock sea un número entero
    
    nuevo_producto['id'] = len(productos) + 1
    productos.append(nuevo_producto)
    
    return jsonify(nuevo_producto), 201

@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    # BUG OCULTO 4: Si el ID no existe, el programa lanza error 500 en vez de 404
    producto = [p for p in productos if p['id'] == id][0]
    return jsonify(producto), 200

if __name__ == '__main__':
    # Escuchamos en todas las interfaces para que Docker funcione
    app.run(host='0.0.0.0', port=5000, debug=True)
