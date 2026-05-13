import pytest

from projeto_1.dominio.base import Insumo, PrecoComposto


@pytest.mark.parametrize("Classe", (Insumo, PrecoComposto))
def test_classe_abstrata_nao_pode_ser_instanciada(Classe):
    error_msg = "Can't instantiate abstract class"
    with pytest.raises(TypeError, match=error_msg):
        Classe()


def test_subclasse_precisa_implementar_metodos_abstratos():
    class SubclasseErrada(Insumo): ...

    error_msg = "Can't instantiate abstract class"
    with pytest.raises(TypeError, match=error_msg):
        SubclasseErrada()

    class SubclasseCerta(Insumo):
        def id(self): ...
        def quantidade(self): ...
        def unidade(self): ...
        def preco_base(self): ...
        def nome(self): ...
        def calcular_total(self): ...
        def __str__(self) -> str:
            return "minha representacao"

    objeto = SubclasseCerta()
    assert str(objeto) == "minha representacao"
