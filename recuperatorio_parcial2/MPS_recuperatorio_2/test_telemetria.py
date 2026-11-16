import pytest
from app_telemetria import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_estado_servicio_ok(client):
    """Verifica que el endpoint de estado responda HTTP 200."""
    response = client.get("/api/v1/estado")
    assert response.status_code == 200
    data = response.get_json()
    assert data["estado"] == "operativo"


def test_telemetria_orbita_no_numerica_debe_retornar_400(client):
    """
    Caja blanca: al enviar un parámetro 'orbita' no numérico (?orbita=abc),
    la API debe validar el tipo de dato y retornar HTTP 400 Bad Request.
    """
    response = client.get("/api/v1/telemetria?orbita=abc")
    assert response.status_code == 400


def test_comando_sin_clave_accion_debe_retornar_400(client):
    """
    Caja blanca: al enviar un payload JSON sin la clave obligatoria 'accion',
    la API debe retornar HTTP 400 Bad Request en lugar de una excepción interna.
    """
    response = client.post(
        "/api/v1/comando",
        json={"objetivo": "antena_principal"}
    )
    assert response.status_code == 400
