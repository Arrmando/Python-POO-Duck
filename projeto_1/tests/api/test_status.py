from litestar.testing import TestClient

from projeto_1.api.app import app


def test_get_status():
    with TestClient(app=app) as client:
        response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
