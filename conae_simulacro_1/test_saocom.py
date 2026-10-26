import pytest
from app_saocom import app

@pytest.fixture
def client():
    """Configura el cliente de pruebas virtual de Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# TEST 1: Ruta raíz del portal web HTML
def test_portal_web_status_code(client):
    """Valida que la página principal responda HTTP 200 OK."""
    respuesta = client.get('/')
    assert respuesta.status_code == 200

# TEST 2: Control de seguridad sin token (401 Unauthorized)
def test_telemetria_sin_token_devuelve_401(client):
    """Valida que acceder a la API sin encabezado Authorization devuelva 401."""
    respuesta = client.get('/api/v1/saocom/telemetria')
    assert respuesta.status_code == 401

# TEST 3: Control de seguridad con token inválido (403 Forbidden)
def test_telemetria_token_falso_devuelve_403(client):
    """CONSIGNA INDIVIDUAL 1: Valida que un token inexistente devuelva HTTP 403 Forbidden."""
    headers = {'Authorization': 'tok-falso-000'}
    respuesta = client.get('/api/v1/saocom/telemetria', headers=headers)
    assert respuesta.status_code == 403

# TEST 4: Perfil OPERADOR (Acceso limitado)
def test_telemetria_operador_exitosa(client):
    """Valida el acceso del perfil OPERADOR y confirma la ausencia de datos orbitales."""
    headers = {'Authorization': 'tok-operador-123'}
    respuesta = client.get('/api/v1/saocom/telemetria', headers=headers)
    datos = respuesta.get_json()
    
    assert respuesta.status_code == 200
    assert datos["estado"] == "OK"
    assert datos["rol_consultante"] == "OPERADOR"
    # El operador NO debe ver datos orbitales
    assert "telemetria_orbital" not in datos["telemetria"][0]

# TEST 5: Perfil ADMINISTRADOR (Acceso completo con telemetría orbital)
def test_telemetria_admin_incluye_datos_orbitales(client):
    """Valida que el perfil ADMINISTRADOR reciba los campos azimut, elevación y altitud."""
    headers = {'Authorization': 'tok-admin-999'}
    respuesta = client.get('/api/v1/saocom/telemetria', headers=headers)
    datos = respuesta.get_json()
    
    assert respuesta.status_code == 200
    assert datos["rol_consultante"] == "ADMINISTRADOR"
    assert "telemetria_orbital" in datos["telemetria"][0]
    
    orbital = datos["telemetria"][0]["telemetria_orbital"]
    assert "azimuth_deg" in orbital
    assert "elevacion_deg" in orbital
    assert "altitud_km" in orbital
    assert "velocidad_kmh" in orbital

# TEST 6: Consigna de validación de login por POST
def test_login_exitoso_admin(client):
    """CONSIGNA INDIVIDUAL 2: Valida el endpoint /api/v1/saocom/login con método POST."""
    payload = {"usuario": "admin", "clave": "satelite99"}
    respuesta = client.post('/api/v1/saocom/login', json=payload)
    datos = respuesta.get_json()
    
    assert respuesta.status_code == 200
    assert datos["estado"] == "OK"
    assert datos["token"] == "tok-admin-999"

def test_descarga_imagen_sin_formato_devuelve_error(client):
    """La prueba espera que la API responda 400 (Bad Request).
    Al estar el bug activo (devuelve 500), este test fallará y Jenkins se pondrá ROJO."""
    respuesta = client.get('/api/v1/saocom/descarga?satelite=SAOCOM_1A&producto=L1B')
    assert respuesta.status_code == 400
