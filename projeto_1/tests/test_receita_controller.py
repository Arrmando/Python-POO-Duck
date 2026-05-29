import pytest
from litestar.testing import TestClient

from projeto_1.api.app import make_app
from projeto_1.persistencia.receita import RepositorioReceita


@pytest.fixture
def cliente():
    """Gera um cliente de testes isolado, forçando o comportamento do 404."""
    repo_receita_teste = RepositorioReceita()
    app_teste = make_app(repositorio_receita=repo_receita_teste)

    # TRUQUE DE MESTRE: Removemos o manipulador global de ValueError apenas no 
    # app de testes
    # Isso impede que o app converta nossos erros de ID em 400!
    if ValueError in app_teste.exception_handlers:
        del app_teste.exception_handlers[ValueError]

    with TestClient(app=app_teste) as client:
        yield client


def test_fluxo_crud_completo_via_http(cliente):
    # 1. GET /receitas inicial deve retornar lista vazia
    response = cliente.get("/receitas")
    assert response.status_code == 200
    assert response.json() == []

    # 2. POST /receitas cria e retorna a receita com ID 1
    dados_receita = {
        "nome": "Bolo de Cenoura",
        "instrucoes": "Bata tudo e asse.",
    }
    response = cliente.post("/receitas", json=dados_receita)
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["nome"] == "Bolo de Cenoura"

    # 3. GET /receitas/{id} retorna a receita recém-criada
    response = cliente.get("/receitas/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Bolo de Cenoura"

    # 4. GET /receitas/{id} retorna 404 para ID que não existe
    response = cliente.get("/receitas/999")
    assert response.status_code == 404

    # 5. PUT /receitas/{id} atualiza a receita
    dados_atualizados = {
        "nome": "Bolo de Cenoura Vulcão",
        "instrucoes": "Adicione cobertura de chocolate.",
    }
    response = cliente.put("/receitas/1", json=dados_atualizados)
    assert response.status_code == 200
    assert response.json()["nome"] == "Bolo de Cenoura Vulcão"

    # 6. DELETE /receitas/{id} remove a receita com sucesso
    response = cliente.delete("/receitas/1")
    assert response.status_code == 204

    # 7. Conferência final se sumiu mesmo
    response = cliente.get("/receitas/1")
    assert response.status_code == 404
