import pytest
from app_saocom import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_portal_web_status_code(client):
    respuesta = client.get('/')
    assert respuesta.status_code == 200

def test_telemetria_sin_token_devuelve_401(client):
    respuesta = client.get('/api/v1/saocom/telemetria?satelite=SAOCOM_1A')
    assert respuesta.status_code == 401

def test_telemetria_token_falso_devuelve_403(client):
    """
    Simulacro 2: Verifica que un token inválido devuelva 403.
    Al estar el Bug 2 activo (lanza KeyError 500), esta prueba FALLARÁ.
    """
    respuesta = client.get('/api/v1/saocom/telemetria?satelite=SAOCOM_1A', 
                           headers={'Authorization': 'Bearer token_invalido_xyz'})
    assert respuesta.status_code == 403  # Fallará porque la API devuelve 500

def test_telemetria_operador_exitosa(client):
    respuesta = client.get('/api/v1/saocom/telemetria?satelite=SAOCOM_1A', 
                           headers={'Authorization': 'Bearer operador_token_123'})
    assert respuesta.status_code == 200

def test_login_exitoso_admin(client):
    respuesta = client.get('/api/v1/saocom/telemetria?satelite=SAOCOM_1A', 
                           headers={'Authorization': 'Bearer admin_token_999'})
    assert respuesta.status_code == 200
