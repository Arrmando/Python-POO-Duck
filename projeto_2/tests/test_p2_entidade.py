import pytest
from projeto_2.model.entidade import Entidade
from projeto_2.model.bomba import Bomba
from projeto_2.model.bandeira import Bandeira
from projeto_2.model.celula import Celula


def test_entidade_nao_pode_ser_instanciada():
    """Garante que a classe abstrata Entidade não pode ser instanciada diretamente."""
    with pytest.raises(TypeError):
        Entidade(1, True, 0)


def test_bomba_instanciacao():
    """Garante que a Bomba é instanciada com os valores corretos e comportamento inicial."""
    bomba = Bomba(1, True, 0)
    assert bomba.id == 1
    assert bomba.status is False
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
    assert bandeira.status is True
    assert bandeira.sprite == 32 * 14


def test_celula_status_inicial_e_cavar():
    """Garante que a célula começa com status True (escondida) e vira False (cavada)."""
    celula = Celula(10)
    assert celula.status is True  # Escondida
    celula.cavar()
    assert celula.status is False # Cavada


def test_celula_multiplas_entidades_tipos_diferentes():
    """Garante que a Célula pode ter uma bomba e uma bandeira ao mesmo tempo."""
    celula = Celula(10, True)
    bomba = Bomba(1, False, 0)
    bandeira = Bandeira(2, True, 0)

    celula.adicionar_bomba(bomba)
    celula.adicionar_bandeira(bandeira)

    assert len(celula.entidades) == 2
    assert celula.obter_entidade(Bomba) == bomba
    assert celula.obter_entidade(Bandeira) == bandeira


def test_celula_proibir_duplicata_mesmo_tipo():
    """Garante que a Célula não permite duas entidades do mesmo tipo."""
    celula = Celula(10, True)
    bomba1 = Bomba(1, False, 0)
    bomba2 = Bomba(3, False, 0)

    celula.adicionar_bomba(bomba1)
    with pytest.raises(ValueError, match="já possui uma bomba"):
        celula.adicionar_bomba(bomba2)

    bandeira1 = Bandeira(2, True, 0)
    bandeira2 = Bandeira(4, True, 0)
    
    celula.adicionar_bandeira(bandeira1)
    with pytest.raises(ValueError, match="já possui uma bandeira"):
        celula.adicionar_bandeira(bandeira2)


def test_celula_remover_entidade_especifica():
    """Garante que a remoção afeta apenas o tipo especificado."""
    celula = Celula(10, True)
    bomba = Bomba(1, False, 0)
    bandeira = Bandeira(2, True, 0)

    celula.adicionar_bomba(bomba)
    celula.adicionar_bandeira(bandeira)

    celula.remover_entidade(Bandeira)
    assert len(celula.entidades) == 1
    assert celula.obter_entidade(Bomba) == bomba
    assert celula.obter_entidade(Bandeira) is None

    celula.remover_entidade(Bomba)
    assert len(celula.entidades) == 0
