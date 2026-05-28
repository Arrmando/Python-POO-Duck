from unittest.mock import MagicMock

import pytest

from projeto_1.dominio.pedido import Pedido
from projeto_1.dominio.relatorio import Relatorio


def test_relatorio_inicializacao_vazia():
    relatorio = Relatorio()
    assert len(relatorio.pedidos) == 0
    assert relatorio.prazo is None


def test_relatorio_inicializacao_com_prazo():
    from datetime import datetime, timedelta

    prazo = datetime.now() + timedelta(days=5)
    relatorio = Relatorio(prazo=prazo)
    assert relatorio.prazo == prazo


def test_relatorio_inicializacao_com_pedidos():
    mock_pedido1 = MagicMock(spec=Pedido)
    mock_pedido2 = MagicMock(spec=Pedido)
    relatorio = Relatorio(pedidos=[mock_pedido1, mock_pedido2])
    assert len(relatorio.pedidos) == 2
    assert mock_pedido1 in relatorio.pedidos
    assert mock_pedido2 in relatorio.pedidos


def test_relatorio_adicionar_pedido():
    relatorio = Relatorio()
    mock_pedido = MagicMock(spec=Pedido)
    relatorio.adicionar_pedido(mock_pedido)
    assert len(relatorio.pedidos) == 1
    assert mock_pedido in relatorio.pedidos


def test_relatorio_adicionar_pedido_invalido():
    relatorio = Relatorio()
    msg = "Apenas objetos do tipo Pedido podem ser adicionados"
    with pytest.raises(ValueError, match=msg):
        relatorio.adicionar_pedido("não é um pedido")


def test_relatorio_remover_pedido():
    mock_pedido = MagicMock(spec=Pedido)
    relatorio = Relatorio(pedidos=[mock_pedido])
    relatorio.remover_pedido(mock_pedido)
    assert len(relatorio.pedidos) == 0


def test_relatorio_remover_pedido_inexistente():
    relatorio = Relatorio()
    mock_pedido = MagicMock(spec=Pedido)
    msg = "O pedido informado não pertence a este relatório"
    with pytest.raises(ValueError, match=msg):
        relatorio.remover_pedido(mock_pedido)


def test_relatorio_calcular_total_geral():
    mock_pedido1 = MagicMock(spec=Pedido)
    mock_pedido1.calcular_total.return_value = 100.0

    mock_pedido2 = MagicMock(spec=Pedido)
    mock_pedido2.calcular_total.return_value = 250.0

    relatorio = Relatorio(pedidos=[mock_pedido1, mock_pedido2])

    assert relatorio.calcular_total_geral() == 350.0
    assert mock_pedido1.calcular_total.call_count == 1
    assert mock_pedido2.calcular_total.call_count == 1


def test_relatorio_gerar_lista_compras():
    # Setup Mocks
    from projeto_1.dominio.base import Insumo
    from projeto_1.dominio.homem_hora import HomemHora
    from projeto_1.dominio.pedido import ItemPedido
    from projeto_1.dominio.receita import ItemReceita, Receita

    # Insumo 1: Farinha, R$ 10.00/kg
    insumo1 = MagicMock(spec=Insumo)
    insumo1.id = 1
    insumo1.preco_base = 10.0

    # Insumo 2: Ovo, R$ 1.00/un
    insumo2 = MagicMock(spec=Insumo)
    insumo2.id = 2
    insumo2.preco_base = 1.0

    # Insumo 3: Confeiteiro (HomemHora), R$ 50.00/h
    insumo3 = MagicMock(spec=HomemHora)
    insumo3.id = 3
    insumo3.preco_base = 50.0

    # Receita A: Usa 2kg Farinha, 3 Ovos e 1h Confeiteiro
    item_rA_1 = MagicMock(spec=ItemReceita)
    item_rA_1.insumo = insumo1
    item_rA_1.coeficiente = 2.0

    item_rA_2 = MagicMock(spec=ItemReceita)
    item_rA_2.insumo = insumo2
    item_rA_2.coeficiente = 3.0

    item_rA_3 = MagicMock(spec=ItemReceita)
    item_rA_3.insumo = insumo3
    item_rA_3.coeficiente = 1.0

    receitaA = MagicMock(spec=Receita)
    receitaA.itens = [item_rA_1, item_rA_2, item_rA_3]

    # Receita B: Usa 1kg Farinha
    item_rB_1 = MagicMock(spec=ItemReceita)
    item_rB_1.insumo = insumo1
    item_rB_1.coeficiente = 1.0

    receitaB = MagicMock(spec=Receita)
    receitaB.itens = [item_rB_1]

    # Pedido 1: 2x Receita A
    item_p1 = MagicMock(spec=ItemPedido)
    item_p1.receita = receitaA
    item_p1.coeficiente = 2.0

    pedido1 = MagicMock(spec=Pedido)
    pedido1.itens = [item_p1]

    # Pedido 2: 1x Receita B
    item_p2 = MagicMock(spec=ItemPedido)
    item_p2.receita = receitaB
    item_p2.coeficiente = 1.0

    pedido2 = MagicMock(spec=Pedido)
    pedido2.itens = [item_p2]

    relatorio = Relatorio(pedidos=[pedido1, pedido2])
    lista = relatorio.gerar_lista_compras()

    # Totais Esperados:
    # Farinha: (2kg * 2) + (1kg * 1) = 5kg. Subtotal: 5 * 10 = 50.0
    # Ovo: (3un * 2) = 6un. Subtotal: 6 * 1 = 6.0
    # Confeiteiro: EXCLUÍDO (mesmo estando na receita)

    assert len(lista) == 2  # Apenas Farinha e Ovo

    farinha_entry = next(item for item in lista if item["insumo"].id == 1)
    ovo_entry = next(item for item in lista if item["insumo"].id == 2)

    # Verifica que não há Confeiteiro na lista
    assert not any(item["insumo"].id == 3 for item in lista)

    assert farinha_entry["quantidade"] == 5.0
    assert farinha_entry["subtotal"] == 50.0

    assert ovo_entry["quantidade"] == 6.0
    assert ovo_entry["subtotal"] == 6.0


def test_relatorio_calcular_prazo_estimado():
    from datetime import datetime, timedelta

    from projeto_1.dominio.homem_hora import HomemHora
    from projeto_1.dominio.pedido import ItemPedido
    from projeto_1.dominio.receita import ItemReceita, Receita

    # Insumo: Padeiro (HomemHora)
    padeiro = MagicMock(spec=HomemHora)

    # Receita: 4 horas de Padeiro
    item_receita = MagicMock(spec=ItemReceita)
    item_receita.insumo = padeiro
    item_receita.coeficiente = 4.0

    receita = MagicMock(spec=Receita)
    receita.itens = [item_receita]

    # Pedido: 2x a Receita (Total = 8 horas)
    item_pedido = MagicMock(spec=ItemPedido)
    item_pedido.receita = receita
    item_pedido.coeficiente = 2.0

    pedido = MagicMock(spec=Pedido)
    pedido.itens = [item_pedido]

    relatorio = Relatorio(pedidos=[pedido])

    # Teste 1: 8 horas totais / 8 horas por dia = 1 dia
    data_base = datetime(2026, 5, 26, 10, 0)
    prazo = relatorio.calcular_prazo_estimado(horas_diarias=8.0, data_inicio=data_base)
    assert prazo == data_base + timedelta(days=1)

    # Teste 2: 8 horas totais / 4 horas por dia = 2 dias
    prazo = relatorio.calcular_prazo_estimado(horas_diarias=4.0, data_inicio=data_base)
    assert prazo == data_base + timedelta(days=2)
