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


def test_post_homem_hora(client):
    r = client.post(
        "/insumo",
        json={
            "tipo": "HomemHora",
            "nome": "Pedreiro",
            "quantidade": 8,
            "preco_base": 50.0,
        },
    )
    assert r.status_code == 201
    assert r.json()["unidade"] == "h"


def test_post_disponivel_em_get(client):
    client.post(
        "/insumo",
        json={
            "tipo": "Ingrediente",
            "nome": "Açúcar",
            "unidade": "kg",
            "quantidade": 1,
            "preco_base": 3.0,
        },
    )
    items = client.get("/insumo").json()
    assert len(items) == 1
    assert items[0]["nome"] == "Açúcar"


def test_post_tipo_invalido(client):
    r = client.post(
        "/insumo",
        json={
            "tipo": "Outro",
            "nome": "X",
            "unidade": "kg",
            "quantidade": 1,
            "preco_base": 1.0,
        },
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Tipo desconhecido: Outro"


def test_post_nome_vazio(client):
    r = client.post(
        "/insumo",
        json={
            "tipo": "Ingrediente",
            "nome": "",
            "unidade": "kg",
            "quantidade": 1,
            "preco_base": 1.0,
        },
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "O nome do ingrediente deve ser uma string não vazia."


def test_post_quantidade_invalida(client):
    r = client.post(
        "/insumo",
        json={
            "tipo": "Ingrediente",
            "nome": "Sal",
            "unidade": "kg",
            "quantidade": 0,
            "preco_base": 1.0,
        },
    )
    assert r.status_code == 400
    assert (
        r.json()["detail"]
        == "A quantidade do ingrediente deve ser um inteiro não negativo."
    )
