import pytest
from unittest.mock import MagicMock
from projeto_1.dominio.pedido import ItemPedido
from projeto_1.dominio.receita import Receita

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
