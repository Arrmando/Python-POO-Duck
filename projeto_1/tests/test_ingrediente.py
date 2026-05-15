import pytest
from src.projeto_1.dominio.ingrediente import Ingrediente

def test_instanciacao_valida():
    ing = Ingrediente("Farinha", "kg", 5, 4.50, id=1)
    assert ing.id == 1
    assert ing.nome == "Farinha"
    assert ing.calcular_total() == 22.50

def test_instanciacao_sem_id():
    ing = Ingrediente("Sal", "un", 10, 1.00)
    assert ing.id is None

def test_id_readonly():
    ing = Ingrediente("Ovo", "un", 12, 0.50, id=10)
    with pytest.raises(AttributeError):
        ing.id = 20

@pytest.mark.parametrize("atributo, valor_invalido", [
    ("nome", ""),
    ("nome", "   "),
    ("unidade", ""),
    ("quantidade", 0),
    ("quantidade", -1),
    ("preco_base", -0.01),
])
def test_setters_invalidos(atributo, valor_invalido):
    ing = Ingrediente("Teste", "un", 1, 1.0)
    with pytest.raises(ValueError):
        setattr(ing, atributo, valor_invalido)

def test_calcular_total():
    ing = Ingrediente("Açúcar", "kg", 2, 5.0)
    assert ing.calcular_total() == 10.0
    ing.quantidade = 3
    assert ing.calcular_total() == 15.0

def test_str_representation():
    ing = Ingrediente("Leite", "L", 2, 4.0, id=5)
    string_rep = str(ing)
    assert "Leite" in string_rep
    assert "L" in string_rep
    assert "8.00" in string_rep