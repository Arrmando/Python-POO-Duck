import pytest

from projeto_1.dominio.base import Insumo


def test_insumo_nao_pode_ser_instanciado():
    error_msg = "Can't instantiate abstract class"
    with pytest.raises(TypeError, match=error_msg):
        Insumo()


def test_subclasse_da_erro_se_nao_implementar_metodos_abstratos():
    class Fake(Insumo): ...

    error_msg = "Can't instantiate abstract class"
    with pytest.raises(TypeError, match=error_msg):
        Fake()


def test_subclasse_instanciada_se_implementa_metodos_abstratos():
    class Fake(Insumo):
        def id(self): ...
        def quantidade(self): ...
        def unidade(self): ...
        def preco_base(self): ...
        def nome(self): ...
        def __str__(self) -> str:
            return "minha representacao"

    objeto = Fake()
    assert str(objeto) == "minha representacao"
