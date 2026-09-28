import pytest
from app_saocom import app, db

@pytest.fixture
def client():
    """Configura un cliente de pruebas virtual de Flask (Caja Blanca / En memoria)."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_endpoint_telemetria_status_code(client):
    """Valida que el endpoint de telemetría responda con código HTTP 200 OK."""
    respuesta = client.get('/api/v1/saocom/telemetria')
    assert respuesta.status_code == 200

def test_endpoint_telemetria_contenido_json(client):
    """Valida la estructura del JSON devuelto por la API."""
    respuesta = client.get('/api/v1/saocom/telemetria')
    datos = respuesta.get_json()
    
    assert datos["estado"] == "OK"
    assert len(datos["telemetria"]) == 2
    assert datos["telemetria"][0]["satelite"] == "SAOCOM-1A"

# -----------------

def test_endpoint_telemetria_estructura_items(client):
    """
    CONSIGNA 1: Validar que cada satélite en la lista tenga las claves
    esperadas ('satelite', 'humedad_suelo_pct', 'estado_radar').
    """
    respuesta = client.get('/api/v1/saocom/telemetria')
    datos = respuesta.get_json()
    primer_satelite = datos["telemetria"][0]
    
    assert "satelite" in primer_satelite
    assert "humedad_suelo_pct" in primer_satelite
    assert "estado_radar" in primer_satelite

def test_portal_web_status_code(client):
    """
    CONSIGNA 2: Validar que la ruta raíz ('/') que renderiza el HTML
    responda con HTTP 200 OK.
    """
    respuesta = client.get('/')
    assert respuesta.status_code == 200