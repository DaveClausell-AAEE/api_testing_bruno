import pytest
from app_saocom import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    """Verifica disponibilidad base de la API."""
    respuesta = client.get('/')
    assert respuesta.status_code == 200

# =========================================================================
# TODO ALUMNO - CASO 1:
# Escribir 'test_solicitud_sin_resolucion_devuelve_400(client)'
# Realizar POST a '/api/v1/saocom/catalogo/solicitud' con JSON:
# {"satelite": "SAOCOM_1A", "sensor_mode": "TOPAR"} (omitiendo 'resolucion')
# y verificar assert respuesta.status_code == 400.
# =========================================================================


# =========================================================================
# TODO ALUMNO - CASO 2:
# Escribir 'test_cuota_api_key_invalida_devuelve_403(client)'
# Realizar GET a '/api/v1/saocom/descarga/cuota'
# enviando cabecera headers={'X-API-Key': 'key_invalida_xyz'}
# y verificar assert respuesta.status_code == 403.
# =========================================================================
