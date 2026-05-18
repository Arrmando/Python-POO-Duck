import pytest
from projeto_1.dominio.homem_hora import HomemHora


def test_instanciacao_valida_com_id():
    """RF: Instanciação com todos os campos válidos (com id)."""
    hh = HomemHora(nome="Cozinheiro", quantidade=10, preco_base=50.0, id=1)
    assert hh.id == 1
    assert hh.nome == "Cozinheiro"
    assert hh.quantidade == 10
    assert hh.preco_base == 50.0
    assert hh.unidade == "h"


def test_instanciacao_valida_sem_id():
    """RF: Instanciação com todos os campos válidos (sem id)."""
    hh = HomemHora(nome="Auxiliar", quantidade=5, preco_base=20.0)
    assert hh.id is None
    assert hh.nome == "Auxiliar"
    assert hh.quantidade == 5
    assert hh.preco_base == 20.0


def test_id_is_readonly():
    """RF: id é read-only (atribuição levanta AttributeError)."""
    hh = HomemHora("Chef", 2, 100.0, id=10)
    with pytest.raises(AttributeError):
        hh.id = 20


def test_unidade_is_readonly():
    """RF: unidade é read-only (atribuição levanta AttributeError)."""
    hh = HomemHora("Cozinheiro", 5, 40.0)
    # A classe HomemHora não possui setter para unidade, logo deve levantar AttributeError
    with pytest.raises(AttributeError):
        hh.unidade = "kg"


@pytest.mark.parametrize(
    "atributo, valor_invalido",
    [
        # Nome inválido (vazio, espaços ou tipo incorreto)
        ("nome", ""),
        ("nome", "   "),
        ("nome", None),
        ("nome", 123),
        # Quantidade inválida (negativa ou tipo incorreto)
        ("quantidade", -1),
        ("quantidade", 1.5),
        ("quantidade", "10"),
        # Preço base inválido (negativo ou tipo incorreto)
        ("preco_base", -0.01),
        ("preco_base", "50.0"),
        ("preco_base", None),
    ],
)
def test_setters_rejeitam_valores_invalidos(atributo, valor_invalido):
    """RF: Setter de cada atributo rejeita valor inválido com ValueError."""
    hh = HomemHora("Teste", 1, 10.0)
    with pytest.raises(ValueError):
        setattr(hh, atributo, valor_invalido)


def test_calcular_total_retorna_valor_correto():
    """RF: calcular_total() retorna o valor correto."""
    hh = HomemHora("Faxineiro", 8, 15.0)
    # 8 * 15.0 = 120.0
    assert hh.calcular_total() == 120.0
    
    # Alterando valores e recalculando
    hh.quantidade = 10
    hh.preco_base = 20.0
    # 10 * 20.0 = 200.0
    assert hh.calcular_total() == 200.0


def test_str_representation():
    """Verifica se a representação em string está amigável."""
    hh = HomemHora("Padeiro", 5, 30.0, id=7)
    assert str(hh) == "Padeiro: 5h x R$ 30.00/h = R$ 150.00"
