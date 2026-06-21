from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = "mars_curiosity_telemetry.db"

def conectar_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  
    return conn

def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    # Crear tabla para el instrumento REMS de Curiosity
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetria_rems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            sensor TEXT,
            presion_atmosferica REAL
        )
    """)
    
    # Inyectar 20 registros históricos (Contiene 2 anomalías intencionales para que el alumno detecte por GET)
    cursor.execute("SELECT COUNT(*) FROM telemetria_rems")
    if cursor.fetchone()[0] == 0:
        datos_historicos = [
            ("REMS_Pressure_Sensor", 712),
            ("REMS_Pressure_Sensor", 685),
            ("REMS_Pressure_Sensor", 740),
            ("REMS_Pressure_Sensor", 615),
            ("REMS_Pressure_Sensor", 890),
            ("REMS_Pressure_Sensor", 775),
            ("REMS_Pressure_Sensor", 630),
            ("REMS_Pressure_Sensor", 520),  # <--- ANOMALÍA 1: ID 8 (Por debajo de 600 Pa)
            ("REMS_Pressure_Sensor", 810),
            ("REMS_Pressure_Sensor", 725),
            ("REMS_Pressure_Sensor", 695),
            ("REMS_Pressure_Sensor", 760),
            ("REMS_Pressure_Sensor", 845),
            ("REMS_Pressure_Sensor", 670),
            ("REMS_Pressure_Sensor", 985),  # <--- ANOMALÍA 2: ID 15 (Por encima de 900 Pa)
            ("REMS_Pressure_Sensor", 730),
            ("REMS_Pressure_Sensor", 610),
            ("REMS_Pressure_Sensor", 805),
            ("REMS_Pressure_Sensor", 790),
            ("REMS_Pressure_Sensor", 865)
        ]
        cursor.executemany("""
            INSERT INTO telemetria_rems (sensor, presion_atmosferica) 
            VALUES (?, ?)
        """, datos_historicos)
        conn.commit()
        
    conn.close()

# --- ENDPOINTS DE LA API (MISIÓN CURIOSITY - INSTRUMENTO REMS) ---

# GET GENERAL: Devuelve el histórico (20 registros iniciales)
@app.route('/telemetria', methods=['GET'])
def obtener_todo():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM telemetria_rems")
    filas = cursor.fetchall()
    conn.close()
    return jsonify([dict(f) for f in filas]), 200

# POST: Intentar registrar telemetría de presión
# BUGS INTENCIONALES: No valida rangos operativos (600-900 Pa), tipos de datos ni payloads vacíos.
@app.route('/telemetria', methods=['POST'])
def registrar_telemetria():
    data = request.get_json()
    
    if data is None:
        data = {}
        
    sensor = data.get('sensor', 'REMS_DEFAULT')
    presion_atmosferica = data.get('presion_atmosferica')
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO telemetria_rems (sensor, presion_atmosferica) VALUES (?, ?)",
        (sensor, presion_atmosferica)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        "id": nuevo_id, 
        "sensor": sensor, 
        "presion_atmosferica": presion_atmosferica,
        "status": "Persistido en DB"
    }), 201

if __name__ == '__main__':
    inicializar_db()
    app.run(host='0.0.0.0', port=5000)
