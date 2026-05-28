import pytest
from litestar.testing import TestClient

from projeto_1.api.app import make_app
from projeto_1.dominio.ingrediente import Ingrediente
from projeto_1.dominio.receita import ItemReceita, Receita
from projeto_1.persistencia.insumo import RepositorioInsumo
from projeto_1.persistencia.receita import RepositorioReceita


@pytest.fixture
def populated_client():
    repo_insumo = RepositorioInsumo()
    repo_receita = RepositorioReceita()

    # Adiciona Insumo
    farinha = Ingrediente("Farinha", "kg", 10, 5.0)
    repo_insumo.save(farinha)

    # Adiciona Receita
    pao = Receita("Pão", "Misture tudo")
    pao.adicionar_item(ItemReceita(farinha, 0.5))
    repo_receita.save(pao)

    with TestClient(app=make_app(repo_insumo, repo_receita)) as c:
        yield c


def test_gerar_relatorio_sucesso(populated_client):
    payload = {"cliente": "Pedro", "itens": [{"receita_id": 1, "quantidade": 2}]}
    r = populated_client.post("/relatorio", json=payload)

    assert r.status_code == 201
    data = r.json()
    assert data["total_geral"] == 5.0
    assert len(data["lista_compras"]) == 1
    assert data["lista_compras"][0]["insumo"] == "Farinha"
    assert data["lista_compras"][0]["quantidade"] == 1.0


def test_gerar_relatorio_receita_inexistente(populated_client):
    payload = {"cliente": "Pedro", "itens": [{"receita_id": 999, "quantidade": 1}]}
    r = populated_client.post("/relatorio", json=payload)
    assert r.status_code == 400
    assert "Receita com ID 999 não encontrada" in r.json()["detail"]
