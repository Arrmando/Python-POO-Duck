import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from projeto_1.dominio.pedido import ItemPedido, Pedido
from projeto_1.dominio.receita import Receita

def test_pedido_datas():
    prazo = datetime.now() + timedelta(days=7)
    pedido = Pedido(cliente="Carlos", prazo_pedido=prazo)
    
    assert isinstance(pedido.data_pedido, datetime)
    assert pedido.prazo_pedido == prazo
    # Verifica se a data do pedido é recente (criada no construtor)
    assert (datetime.now() - pedido.data_pedido).total_seconds() < 1

def test_pedido_data_pedido_readonly():
    pedido = Pedido(cliente="Carlos")
    with pytest.raises(AttributeError):
        pedido.data_pedido = datetime.now()

def test_item_pedido_criacao_valida():
    mock_receita = MagicMock(spec=Receita)
    coeficiente = 2.5
    item = ItemPedido(receita=mock_receita, coeficiente=coeficiente)
    
    assert item.receita == mock_receita
    assert item.coeficiente == coeficiente

def test_item_pedido_receita_nula_deve_levantar_erro():
    with pytest.raises(ValueError, match="O item da receita precisa estar vinculado a uma receita válida"):
        ItemPedido(receita=None, coeficiente=1.0)

def test_item_pedido_coeficiente_invalido_deve_levantar_erro():
    mock_receita = MagicMock(spec=Receita)
    
    with pytest.raises(ValueError, match="O coeficiente do item deve ser maior que zero"):
        ItemPedido(receita=mock_receita, coeficiente=0)
        
    with pytest.raises(ValueError, match="O coeficiente do item deve ser maior que zero"):
        ItemPedido(receita=mock_receita, coeficiente=-1.0)

def test_item_pedido_calcular_total_dinamico():
    mock_receita = MagicMock(spec=Receita)
    coeficiente = 2.0
    item = ItemPedido(receita=mock_receita, coeficiente=coeficiente)
    
    # Primeiro cálculo
    mock_receita.calcular_total.return_value = 100.0
    assert item.calcular_total() == 200.0
    
    # Segundo cálculo com novo valor na receita
    mock_receita.calcular_total.return_value = 150.0
    assert item.calcular_total() == 300.0
    
    assert mock_receita.calcular_total.call_count == 2

def test_pedido_criacao_e_manipulacao_itens():
    mock_receita1 = MagicMock(spec=Receita)
    mock_receita1.calcular_total.return_value = 50.0
    item1 = ItemPedido(receita=mock_receita1, coeficiente=2.0) # 100.0

    mock_receita2 = MagicMock(spec=Receita)
    mock_receita2.calcular_total.return_value = 30.0
    item2 = ItemPedido(receita=mock_receita2, coeficiente=1.0) # 30.0

    pedido = Pedido(cliente="João Silva")
    
    pedido.adicionar_item(item1)
    pedido.adicionar_item(item2)

    assert pedido.cliente == "João Silva"
    assert len(pedido.itens) == 2
    assert pedido.calcular_total() == 130.0

    pedido.remover_item(item1)
    assert len(pedido.itens) == 1
    assert pedido.calcular_total() == 30.0

def test_pedido_cliente_vazio_deve_levantar_erro():
    with pytest.raises(ValueError, match="O nome do cliente não pode ser vazio"):
        Pedido(cliente="")
    with pytest.raises(ValueError, match="O nome do cliente não pode ser vazio"):
        Pedido(cliente="   ")

def test_pedido_remover_item_inexistente_deve_levantar_erro():
    mock_receita = MagicMock(spec=Receita)
    item = ItemPedido(receita=mock_receita, coeficiente=1.0)
    item_fora = ItemPedido(receita=mock_receita, coeficiente=2.0)
    
    pedido = Pedido(cliente="Maria")
    pedido.adicionar_item(item)
    
    with pytest.raises(ValueError, match="O item informado não pertence a este pedido"):
        pedido.remover_item(item_fora)

def test_pedido_adicionar_item_invalido_deve_levantar_erro():
    pedido = Pedido(cliente="José")
    with pytest.raises(ValueError, match="Apenas objetos do tipo ItemPedido podem ser adicionados"):
        pedido.adicionar_item("não é um item")
