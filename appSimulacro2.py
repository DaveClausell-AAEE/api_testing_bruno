from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = "parker_telemetry.db"

def conectar_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  
    return conn

def inicializar_db():
    conn = conectar_db()
    cursor = conn.cursor()
    # 1. Crear la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetria_parker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instrumento TEXT,
            temperatura_escudo REAL,
            paneles_energia INTEGER
        )
    """)
    
    # 2. Verificar si la base de datos está vacía para inyectar estado inicial real
    cursor.execute("SELECT COUNT(*) FROM telemetria_parker")
    if cursor.fetchone()[0] == 0:
        telemetria_inicial = [
            ("FIELDS (Solar Wind Analyzer)", 24.5, 85),
            ("WISPR (Heliospheric Imager)", 18.2, 90),
            ("SWEAP (Electron/Proton/Alpha)", 31.0, 75)
        ]
        cursor.executemany("""
            INSERT INTO telemetria_parker (instrumento, temperatura_escudo, paneles_energia) 
            VALUES (?, ?, ?)
        """, telemetria_inicial)
        conn.commit()
        
    conn.close()

# --- ENDPOINTS DE LA API (MISIÓN PARKER SOLAR PROBE) ---

@app.route('/telemetria', methods=['GET'])
def obtener_todo():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM telemetria_parker")
    filas = cursor.fetchall()
    conn.close()
    return jsonify([dict(f) for f in filas]), 200

# BUG 1 INTENCIONAL (Error 500): Rompe críticamente si el registro consultado no existe en DB al hacer dict(None)
@app.route('/telemetria/<int:registro_id>', methods=['GET'])
def obtener_por_id(registro_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM telemetria_parker WHERE id = ?", (registro_id,))
    fila = cursor.fetchone()
    conn.close()
    return jsonify(dict(fila)), 200

# BUG 2 y 3 INTENCIONALES: Falsos positivos (201 Created). El sistema no valida rangos físicos ni consistencia de tipos
@app.route('/telemetria', methods=['POST'])
def registrar_telemetria():
    data = request.get_json()
    instrumento = data.get('instrumento')
    temperatura_escudo = data.get('temperatura_escudo')
    paneles_energia = data.get('paneles_energia')
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO telemetria_parker (instrumento, temperatura_escudo, paneles_energia) VALUES (?, ?, ?)",
        (instrumento, temperatura_escudo, paneles_energia)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"id": nuevo_id, "instrumento": instrumento, "temperatura_escudo": temperatura_escudo, "paneles_energia": paneles_energia}), 201

if __name__ == '__main__':
    inicializar_db()
    app.run(host='0.0.0.0', port=5000)
