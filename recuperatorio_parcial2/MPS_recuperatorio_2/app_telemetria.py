from flask import Flask, request, jsonify

app = Flask(__name__)

# Datos simulados de telemetría satelital
TELEMETRIA_DB = {
    550: {"orbita_km": 550, "temperatura_c": -12.4, "bateria_pct": 94, "estado": "NOMINAL"},
    600: {"orbita_km": 600, "temperatura_c": -18.1, "bateria_pct": 89, "estado": "NOMINAL"},
}


@app.route("/api/v1/estado", methods=["GET"])
def obtener_estado():
    """Endpoint saludable para verificación básica del servicio."""
    return jsonify({
        "servicio": "Telemetria Satelital",
        "estado": "operativo",
        "version": "1.0.0"
    }), 200


@app.route("/api/v1/telemetria", methods=["GET"])
def consultar_telemetria():
    """
    Consulta datos de telemetría según altura de órbita (?orbita=550).
    DEFECTO SEMBRADO 1 (TEL-BUG-01):
    Convierte directamente a int() sin bloque try/except ni validación previa.
    Si recibe un valor no numérico (ej. ?orbita=abc) o nulo, lanza ValueError/TypeError
    provocando un HTTP 500 Internal Server Error en lugar de HTTP 400 Bad Request.
    """
    orbita_raw = request.args.get("orbita")
    orbita = int(orbita_raw)  # <-- Línea vulnerable: ValueError / TypeError no capturado

    datos = TELEMETRIA_DB.get(orbita)
    if not datos:
        return jsonify({"error": f"No hay registros para la órbita {orbita} km"}), 404

    return jsonify(datos), 200


@app.route("/api/v1/comando", methods=["POST"])
def enviar_comando():
    """
    Envía un comando operativo al satélite mediante JSON: {"accion": "calibrar"}.
    DEFECTO SEMBRADO 2 (TEL-BUG-02):
    Accede directamente a la clave 'accion' mediante indexación de diccionario sin usar .get()
    ni validar el payload. Ante un JSON sin la clave 'accion', lanza KeyError -> HTTP 500.
    """
    payload = request.get_json(silent=True) or {}
    accion = payload["accion"]  # <-- Línea vulnerable: KeyError si falta 'accion'

    acciones_validas = ["calibrar", "reiniciar_sensor", "modo_seguro"]
    if accion not in acciones_validas:
        return jsonify({"error": f"Acción '{accion}' no reconocida"}), 400

    return jsonify({
        "resultado": "comando_aceptado",
        "accion_ejecutada": accion
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
