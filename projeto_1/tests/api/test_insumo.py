import pytest


class TestPost:
    def test_ingrediente(self, client):
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

    def test_homem_hora(self, client):
        r = client.post(
            "/insumo",
            json={
                "tipo": "HomemHora",
                "nome": "Cozinheiro",
                "quantidade": 8,
                "preco_base": 50.0,
            },
        )
        assert r.status_code == 201
        assert r.json()["unidade"] == "h"

    def test_disponivel_em_get(self, client):
        # adiciona primeiro insumo
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
        assert items[0]["id"] == 1

        # adiciona mais um insumo
        client.post(
            "/insumo",
            json={
                "tipo": "HomemHora",
                "nome": "Cozinheiro",
                "quantidade": 8,
                "preco_base": 50.0,
            },
        )
        items = client.get("/insumo").json()
        assert len(items) == 2
        assert items[1]["nome"] == "Cozinheiro"
        assert items[1]["id"] == 2

    @pytest.mark.parametrize(
        "payload, detail",
        [
            pytest.param(
                {
                    "tipo": "Outro",
                    "nome": "X",
                    "unidade": "kg",
                    "quantidade": 1,
                    "preco_base": 1.0,
                },
                "Tipo desconhecido: Outro",
                id="tipo_invalido",
            ),
            pytest.param(
                {
                    "tipo": "Ingrediente",
                    "nome": "",
                    "unidade": "kg",
                    "quantidade": 1,
                    "preco_base": 1.0,
                },
                "O nome do ingrediente deve ser uma string não vazia.",
                id="nome_vazio",
            ),
            pytest.param(
                {
                    "tipo": "Ingrediente",
                    "nome": "Sal",
                    "unidade": "kg",
                    "quantidade": 0,
                    "preco_base": 1.0,
                },
                "A quantidade do ingrediente deve ser um inteiro não negativo.",
                id="quantidade_invalida",
            ),
        ],
    )
    def test_validacao_retorna_400(self, client, payload, detail):
        r = client.post("/insumo", json=payload)
        assert r.status_code == 400
        assert r.json()["detail"] == detail
