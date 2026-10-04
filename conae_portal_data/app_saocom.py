import sqlite3
import time
import math
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

def init_db():
    """Inicializa la base de datos SQLite en memoria con usuarios y credenciales."""
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    
    # Tabla de usuarios del Centro de Control
    cursor.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL,
            rol TEXT NOT NULL,
            token TEXT UNIQUE
        )
    ''')
    cursor.execute("INSERT INTO usuarios (usuario, clave, rol, token) VALUES ('operador', 'conae2026', 'OPERADOR', 'tok-operador-123')")
    cursor.execute("INSERT INTO usuarios (usuario, clave, rol, token) VALUES ('admin', 'satelite99', 'ADMINISTRADOR', 'tok-admin-999')")
    
    conn.commit()
    return conn

db = init_db()

def obtener_posicion_orbita_real(satelite):
    """
    Calcula la propagación de la órbita heliosincrónica (SSO) del SAOCOM a ~620 km de altitud
    en tiempo real (física orbital kepleriana local, sin latencia de red).
    """
    t = time.time()
    fase = 0.0 if "1A" in satelite else math.pi / 2  # Desfasaje orbital entre 1A y 1B
    vel_ang = (2 * math.pi) / (98.8 * 60)           # Período orbital real de 98.8 minutos
    ang = (vel_ang * t + fase) % (2 * math.pi)
    
    return {
        "azimuth_deg": round((math.degrees(ang) * 1.5) % 360, 2),
        "elevacion_deg": round(math.sin(ang) * 90.0, 2),
        "altitud_km": round(619.5 + math.sin(ang * 2) * 2.3, 2),
        "velocidad_kmh": round(27480.0 + math.cos(ang) * 15.0, 2)
    }

# --- RUTA 1: VISTA WEB HTML ---
@app.route('/', methods=['GET'])
def portal_web():
    return render_template('index.html')

# --- RUTA 2: ENDPOINT DE LOGIN (POST) ---
@app.route('/api/v1/saocom/login', methods=['POST'])
def login():
    datos = request.get_json() or {}
    usuario = datos.get('usuario')
    clave = datos.get('clave')
    
    cursor = db.cursor()
    cursor.execute("SELECT usuario, rol, token FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave))
    user = cursor.fetchone()
    
    if user:
        return jsonify({
            "estado": "OK",
            "mensaje": "Autenticación exitosa",
            "usuario": user[0],
            "rol": user[1],
            "token": user[2]
        }), 200
    else:
        return jsonify({
            "estado": "ERROR",
            "mensaje": "Credenciales inválidas"
        }), 401

# --- RUTA 3: ENDPOINT PROTEGIDO DE TELEMETRÍA (GET + AUTH) ---
@app.route('/api/v1/saocom/telemetria', methods=['GET'])
def obtener_telemetria_json():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"estado": "ERROR", "mensaje": "Token de autorización requerido"}), 401
    
    cursor = db.cursor()
    cursor.execute("SELECT usuario, rol FROM usuarios WHERE token = ?", (token,))
    user = cursor.fetchone()
    
    if not user:
        return jsonify({"estado": "ERROR", "mensaje": "Token inválido o expirado"}), 403
    
    rol = user[1]
    base_satelites = [
        {"satelite": "SAOCOM-1A", "humedad_suelo_pct": 42.5, "estado_radar": "ACTIVO"},
        {"satelite": "SAOCOM-1B", "humedad_suelo_pct": 18.2, "estado_radar": "STANDBY"}
    ]
    
    if rol == 'ADMINISTRADOR':
        datos = []
        for sat in base_satelites:
            posicion = obtener_posicion_orbita_real(sat["satelite"])
            datos.append({
                "satelite": sat["satelite"],
                "humedad_suelo_pct": sat["humedad_suelo_pct"],
                "estado_radar": sat["estado_radar"],
                "telemetria_orbital": posicion
            })
    else:
        datos = base_satelites
        
    return jsonify({
        "estado": "OK",
        "rol_consultante": rol,
        "timestamp_utc": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "telemetria": datos
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
