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

# =========================================================================
# TODO ALUMNO (SIMULACRO 1):
# Escribir la prueba unitaria 'test_descarga_sin_formato_devuelve_400(client)'
# Requerimiento: Realizar GET a '/api/v1/saocom/descarga?satelite=SAOCOM_1A'
# (omitiendo el parámetro obligatorio 'producto') y verificar assert respuesta.status_code == 400.
# =========================================================================
