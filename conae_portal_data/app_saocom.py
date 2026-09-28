import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

def init_db():
    """Inicializa la base de datos SQLite en memoria con datos de prueba."""
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE telemetria_saocom (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            satelite TEXT NOT NULL,
            humedad_suelo_pct REAL NOT NULL,
            estado_radar TEXT NOT NULL
        )
    ''')
    
    cursor.execute("INSERT INTO telemetria_saocom (satelite, humedad_suelo_pct, estado_radar) VALUES ('SAOCOM-1A', 42.5, 'ACTIVO')")
    cursor.execute("INSERT INTO telemetria_saocom (satelite, humedad_suelo_pct, estado_radar) VALUES ('SAOCOM-1B', 18.2, 'STANDBY')")
    
    conn.commit()
    return conn

db = init_db()

# --- RUTA 1: RUTA WEB PARA EL NAVEGADOR (Página bonita) ---
@app.route('/', methods=['GET'])
def portal_web():
    cursor = db.cursor()
    cursor.execute("SELECT satelite, humedad_suelo_pct, estado_radar FROM telemetria_saocom")
    filas = cursor.fetchall()
    datos = [{"satelite": f[0], "humedad_suelo_pct": f[1], "estado_radar": f[2]} for f in filas]
    
    # render_template busca el archivo index.html dentro de la carpeta /templates
    return render_template('index.html', telemetria=datos)

# --- RUTA 2: ENDPOINT DE API (Para Bruno CLI / PyTest / Tests de integración) ---
@app.route('/api/v1/saocom/telemetria', methods=['GET'])
def obtener_telemetria_json():
    cursor = db.cursor()
    cursor.execute("SELECT satelite, humedad_suelo_pct, estado_radar FROM telemetria_saocom")
    filas = cursor.fetchall()
    datos = [{"satelite": f[0], "humedad_suelo_pct": f[1], "estado_radar": f[2]} for f in filas]
    return jsonify({"estado": "OK", "telemetria": datos}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)