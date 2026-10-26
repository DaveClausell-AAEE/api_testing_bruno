from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Base de datos simulada de telemetría SAOCOM
TELEMETRIA_DB = {
    "SAOCOM_1A": {"estado": "NOMINAL", "bateria_v": 28.4, "temperatura_c": 18.2, "orbita_altitud_km": 620.5},
    "SAOCOM_1B": {"estado": "NOMINAL", "bateria_v": 28.1, "temperatura_c": 19.0, "orbita_altitud_km": 621.1}
}

VALID_TOKENS = {
    "operador_token_123": "OPERADOR",
    "admin_token_999": "ADMIN"
}

@app.route('/')
def home():
    return """
    <html>
        <head><title>CONAE - Portal SAOCOM v3.0</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>🛰️ CONAE - Portal de Control SAOCOM (Simulacro 2)</h1>
            <p>Estado del sistema: <b style="color: green;">ONLINE</b></p>
            <ul>
                <li>API Telemetría: <code>/api/v1/saocom/telemetria</code></li>
                <li>API Descargas: <code>/api/v1/saocom/descarga</code></li>
            </ul>
        </body>
    </html>
    """

@app.route('/api/v1/saocom/telemetria', methods=['GET'])
def obtener_telemetria():
    satelite = request.args.get('satelite')
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "No autorizado", "mensaje": "Se requiere cabecera Authorization"}), 401

    token_limpio = token.replace('Bearer ', '')

    # -------------------------------------------------------------------------
    # BUG SIMULACRO 2: Si el token es falso o invalido, rompe con 500 (KeyError)
    # Comportamiento esperado: Debería devolver HTTP 403 Forbidden
    # -------------------------------------------------------------------------
    if token_limpio not in VALID_TOKENS:
        # Forzar excepcion de servidor (Uncaught KeyError)
        rol = VALID_TOKENS[token_limpio]  # <--- Provoca KeyError -> HTTP 500

    rol = VALID_TOKENS[token_limpio]
    datos = TELEMETRIA_DB.get(satelite, TELEMETRIA_DB["SAOCOM_1A"])
    
    if rol == "OPERADOR":
        # Operador no ve altitud de orbita
        datos_filtrados = {k: v for k, v in datos.items() if k != "orbita_altitud_km"}
        return jsonify({"satelite": satelite, "rol": rol, "telemetria": datos_filtrados}), 200

    return jsonify({"satelite": satelite, "rol": rol, "telemetria": datos}), 200

@app.route('/api/v1/saocom/descarga', methods=['GET'])
def descargar_imagen():
    satelite = request.args.get('satelite')
    producto = request.args.get('producto')
    formato = request.args.get('formato')

    # En Simulacro 2, la descarga valida correctamente los parametros
    if not formato:
        return jsonify({"error": "Bad Request", "mensaje": "El parámetro 'formato' es obligatorio"}), 400

    return jsonify({"status": "SUCCESS", "satelite": satelite, "producto": producto, "formato": formato}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
