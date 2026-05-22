import pytest

from projeto_1.dominio.base import Insumo, Item, PrecoComposto


@pytest.mark.parametrize("Classe", (Insumo, PrecoComposto, Item))
def test_classe_abstrata_nao_pode_ser_instanciada(Classe):
    error_msg = "Can't instantiate abstract class"
    with pytest.raises(TypeError, match=error_msg):
        Classe()


def test_item_coeficiente_heranca():
    class SubItem(Item):
        @property
        def coeficiente(self) -> float:
            return 2.5

        def calcular_total(self) -> float:
            return 10.0

    item = SubItem()
    assert item.coeficiente == 2.5
    assert item.calcular_total() == 10.0


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
