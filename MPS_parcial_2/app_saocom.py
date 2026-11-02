from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Base de datos simulada para claves API
API_KEYS_VALIDAS = {
    "key_operador_123": "OPERADOR",
    "key_admin_999": "ADMIN"
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "OK", "servicio": "Portal SAOCOM - Parcial 2"}), 200


# 🔴 CASO 1: Solicitud de Catálogo (Falta de 'resolucion' -> HTTP 500)
@app.route('/api/v1/saocom/catalogo/solicitud', methods=['POST'])
def solicitar_catalogo():
    data = request.get_json() or {}
    
    satelite = data.get('satelite')
    sensor_mode = data.get('sensor_mode')
    resolucion = data.get('resolucion')
    
    # Validaciones básicas que sí funcionan bien (devuelven 400)
    if not satelite or not sensor_mode:
        return jsonify({"error": "Bad Request", "mensaje": "Los campos 'satelite' y 'sensor_mode' son obligatorios"}), 400

    # BUG PARCIAL 2: Si falta 'resolucion', provoca un fallo interno (HTTP 500)
    if not resolucion:
        return jsonify({
            "error": "Internal Server Error",
            "message": "NullPointerException: Campo obligatorio 'resolucion' no especificado en el payload JSON"
        }), 500

    return jsonify({
        "status": "PROCESANDO",
        "satelite": satelite,
        "sensor_mode": sensor_mode,
        "resolucion": resolucion,
        "ticket_id": "REQ-2026-99"
    }), 200


# 🔵 CASO 2: Cuota de Descarga (API Key Inválida -> KeyError / HTTP 500)
@app.route('/api/v1/saocom/descarga/cuota', methods=['GET'])
def consultar_cuota():
    api_key = request.headers.get('X-API-Key')
    
    if not api_key:
        return jsonify({"error": "No Autorizado", "mensaje": "Se requiere cabecera X-API-Key"}), 401
    
    # BUG PARCIAL 2: Si la API Key no es válida, no usa .get() ni try/except,
    # sino indexación directa que lanza KeyError (HTTP 500)
    if api_key not in API_KEYS_VALIDAS:
        rol = API_KEYS_VALIDAS[api_key]  # <--- Provoca KeyError -> HTTP 500
        
    rol = API_KEYS_VALIDAS[api_key]
    return jsonify({
        "status": "OK",
        "api_key": api_key,
        "rol": rol,
        "cuota_diaria_restante_gb": 150
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('FLASK_RUN_PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
