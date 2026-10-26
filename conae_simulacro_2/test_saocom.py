import pytest
from app_saocom import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_portal_web_status_code(client):
    """Verifica la disponibilidad base del portal SAOCOM."""
    respuesta = client.get('/')
    assert respuesta.status_code == 200

def test_telemetria_sin_token_devuelve_401(client):
    """Verifica que la falta total de cabecera responda 401."""
    respuesta = client.get('/api/v1/saocom/telemetria?satelite=SAOCOM_1A')
    assert respuesta.status_code == 401

# =========================================================================
# TODO ALUMNO (SIMULACRO 2):
# Escribir la prueba unitaria 'test_telemetria_token_invalido_devuelve_403(client)'
# Requerimiento: Realizar GET a '/api/v1/saocom/telemetria?satelite=SAOCOM_1A'
# enviando cabecera headers={'Authorization': 'Bearer token_trucho_123'}
# y verificar assert respuesta.status_code == 403.
# =========================================================================
