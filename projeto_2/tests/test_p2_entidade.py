import pytest
from projeto_2.model.entidade import Entidade
from projeto_2.model.bomba import Bomba
from projeto_2.model.bandeira import Bandeira


def test_entidade_nao_pode_ser_instanciada():
    """Garante que a classe abstrata Entidade não pode ser instanciada diretamente."""
    with pytest.raises(TypeError):
        Entidade(1, True, 0)


def test_bomba_instanciacao():
    """Garante que a Bomba é instanciada com os valores corretos e comportamento inicial."""
    bomba = Bomba(1, True, 0)
    assert bomba.id == 1
    assert bomba.status is False  # Conforme definido no __init__ da Bomba
    assert bomba.sprite == 32 * 2


def test_bomba_explodir():
    """Garante que o método explodir altera o status e o sprite da bomba."""
    bomba = Bomba(1, False, 0)
    bomba.explodir()
    assert bomba.status is True
    assert bomba.sprite == 32 * 3


def test_bandeira_instanciacao():
    """Garante que a Bandeira é instanciada com os valores corretos."""
    bandeira = Bandeira(2, False, 0)
    assert bandeira.id == 2
    assert bandeira.status is True  # Conforme definido no __init__ da Bandeira
    assert bandeira.sprite == 32 * 14
