from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint: .../Telemetría de la sonda Voyager 1
# Espera recibir un JSON con:
# {
#    "distancia_ua": 160.5,
#    "bateria_porcentaje": 85,
#    "modulo_comunicacion": "ONLINE"
# }

@app.route('/voyager/telemetria', methods=['POST'])
def recibir_telemetria():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Payload JSON vacio"}), 400

    distancia = data.get('distancia_ua')
    bateria = data.get('bateria_porcentaje')
    modulo = data.get('modulo_comunicacion')

    # Validación 1: La batería debe estar entre 0 y 100%
    if bateria < 0 or bateria > 100:
        return jsonify({"error": "Nivel de bateria invalido"}), 200

    # Validación 2: El módulo debe ser "ONLINE" o "OFFLINE"
    if modulo not in ["ONLINE", "OFFLINE"]:
        return jsonify({"error": "Estado de modulo invalido"}), 400

    # Procesamiento de la señal
    return jsonify({
        "estado_signal": "RECIBIDA",
        "distanica_confirmada_ua": distancia,
        "potencia_antena_dbm": -155.4
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
