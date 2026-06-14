from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = "parker_sweap_telemetry.db"

def conectar_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  
    return conn

def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    # 1. Crear la tabla si no existe para el instrumento SWEAP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetria_sweap (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            componente TEXT,
            velocidad_viento REAL
        )
    """)
    
    # 2. Inyectar el histórico inicial con 10 datos reales de velocidad del viento solar (SWEAP / Solar Probe Cup)
    cursor.execute("SELECT COUNT(*) FROM telemetria_sweap")
    if cursor.fetchone()[0] == 0:
        datos_historicos = [
            ("Solar Probe Cup (SPC)", 350),
            ("Solar Probe Cup (SPC)", 420),
            ("Solar Probe Cup (SPC)", 510),
            ("Solar Probe Cup (SPC)", 315),
            ("Solar Probe Cup (SPC)", 780),
            ("Solar Probe Cup (SPC)", 640),
            ("Solar Probe Cup (SPC)", 495),
            ("Solar Probe Cup (SPC)", 580),
            ("Solar Probe Cup (SPC)", 710),
            ("Solar Probe Cup (SPC)", 390)
        ]
        cursor.executemany("""
            INSERT INTO telemetria_sweap (componente, velocidad_viento) 
            VALUES (?, ?)
        """, datos_historicos)
        conn.commit()
        
    conn.close()

# --- ENDPOINTS DE LA API (MISIÓN PARKER - INSTRUMENTO SWEAP) ---

# GET GENERAL: Devuelve el histórico de datos (Inicia con los 10 registros científicos)
@app.route('/telemetria', methods=['GET'])
def obtener_todo():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM telemetria_sweap")
    filas = cursor.fetchall()
    conn.close()
    return jsonify([dict(f) for f in filas]), 200


# POST: Registrar telemetría del viento solar
# BUGS INTENCIONALES: No valida tipos de datos (Strings), campos vacíos ni rangos de negocio (300-800 km/s).
# Devuelve falsos positivos (201 Created) ante datos corruptos.
@app.route('/telemetria', methods=['POST'])
def registrar_telemetria():
    data = request.get_json()
    
    # Si el payload es un JSON vacío o inválido, Flask podría no lanzar error aquí
    if data is None:
        data = {}
        
    componente = data.get('componente', 'SWEAP_GENERIC')
    velocidad_viento = data.get('velocidad_viento')
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO telemetria_sweap (componente, velocidad_viento) VALUES (?, ?)",
        (componente, velocidad_viento)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        "id": nuevo_id, 
        "componente": componente, 
        "velocidad_viento": velocidad_viento,
        "status": "Persistido en DB"
    }), 201

if __name__ == '__main__':
    inicializar_db()
    app.run(host='0.0.0.0', port=5000)
