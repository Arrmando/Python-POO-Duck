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
