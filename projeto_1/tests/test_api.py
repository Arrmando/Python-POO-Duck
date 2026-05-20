import pytest
from litestar.testing import TestClient

from projeto_1.api.app import app, make_app
from projeto_1.persistencia.insumo import RepositorioInsumo


def test_get_status():
    with TestClient(app=app) as client:
        response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.fixture
def client():
    with TestClient(app=make_app(RepositorioInsumo())) as c:
        yield c


def test_post_ingrediente(client):
    r = client.post(
        "/insumo",
        json={
            "tipo": "Ingrediente",
            "nome": "Farinha",
            "unidade": "kg",
            "quantidade": 2,
            "preco_base": 5.0,
        },
    )
    assert r.status_code == 201
    assert r.json()["id"] == 1
