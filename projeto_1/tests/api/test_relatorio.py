import pytest
from litestar.testing import TestClient

from projeto_1.api.app import make_app
from projeto_1.dominio.homem_hora import HomemHora
from projeto_1.dominio.ingrediente import Ingrediente
from projeto_1.dominio.receita import ItemReceita, Receita
from projeto_1.persistencia.insumo import RepositorioInsumo
from projeto_1.persistencia.receita import RepositorioReceita


class TestRelatorioAPI:
    @pytest.fixture
    def setup_data(self):
        repo_insumo = RepositorioInsumo()
        repo_receita = RepositorioReceita()

        # Criar insumos
        farinha = Ingrediente("Farinha", "kg", 10, 5.0)
        ovo = Ingrediente("Ovo", "un", 12, 1.0)
        padeiro = HomemHora("Padeiro", 1, 50.0)

        repo_insumo.save(farinha)
        repo_insumo.save(ovo)
        repo_insumo.save(padeiro)

        # Criar Receita
        pao = Receita("Pão", "Misture tudo e asse")
        pao.adicionar_item(ItemReceita(farinha, 0.5))  # 0.5kg farinha = 2.50
        pao.adicionar_item(ItemReceita(ovo, 1.0))  # 1 ovo = 1.00
        pao.adicionar_item(ItemReceita(padeiro, 0.5))  # 0.5h padeiro = 25.00
        # Total pao = 28.50 (sendo 3.50 de ingredientes e 25.00 de mão de obra)

        repo_receita.save(pao)

        return repo_insumo, repo_receita

    @pytest.fixture
    def client(self, setup_data):
        repo_insumo, repo_receita = setup_data
        with TestClient(app=make_app(repo_insumo, repo_receita)) as c:
            yield c

    def test_gerar_relatorio_sucesso(self, client):
        # Payload: 2 pedidos de 10 pães cada
        payload = [
            {"cliente": "João", "itens": [{"receita_id": 1, "coeficiente": 10.0}]},
            {"cliente": "Maria", "itens": [{"receita_id": 1, "coeficiente": 10.0}]},
        ]

        response = client.post("/relatorio", json=payload)

        assert response.status_code == 201
        data = response.json()

        # Total geral = (28.50 * 10) * 2 = 570.0
        assert data["total_geral"] == 570.0

        # Lista de compras (apenas ingredientes físicos)
        # Farinha: 0.5kg * 10 * 2 = 10kg. Subtotal: 10 * 5.0 = 50.0
        # Ovo: 1un * 10 * 2 = 20un. Subtotal: 20 * 1.0 = 20.0
        assert len(data["lista_compras"]) == 2

        farinha_item = next(
            i for i in data["lista_compras"] if i["insumo"]["nome"] == "Farinha"
        )

        assert farinha_item["quantidade"] == 10.0
        assert farinha_item["subtotal"] == 50.0

        # Prazo estimado
        # Total horas = 0.5h * 10 * 2 = 10 horas
        # 10 horas / 8 horas por dia = 1.25 dias
        assert "prazo_estimado" in data
        assert data["prazo_estimado"] is not None

    def test_gerar_relatorio_receita_inexistente(self, client):
        payload = [
            {
                "cliente": "Inexistente",
                "itens": [{"receita_id": 999, "coeficiente": 1.0}],
            }
        ]

        response = client.post("/relatorio", json=payload)

        assert response.status_code == 400
        assert "Receita com ID 999 não encontrada" in response.json()["detail"]
