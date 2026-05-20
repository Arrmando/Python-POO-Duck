import pytest
from litestar.testing import TestClient

from projeto_1.api.app import make_app
from projeto_1.persistencia.insumo import RepositorioInsumo


@pytest.fixture
def client():
    with TestClient(app=make_app(RepositorioInsumo())) as c:
        yield c
