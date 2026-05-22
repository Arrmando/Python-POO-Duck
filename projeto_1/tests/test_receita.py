import pytest
from src.projeto_1.dominio.ingrediente import Ingrediente
from src.projeto_1.dominio.receita import ItemReceita, Receita


def test_criar_receita_e_manipular_itens():
    # 1. Criando os insumos bases para o teste
    acucar = Ingrediente(nome="Açúcar", unidade="kg", quantidade=10, preco_base=4.0)
    farinha = Ingrediente(nome="Farinha", unidade="kg", quantidade=5, preco_base=5.0)

    # 2. Criando os itens da receita (passando o coeficiente)
    item1 = ItemReceita(insumo=acucar, coeficiente=2.0)
    item2 = ItemReceita(insumo=farinha, coeficiente=3.0)

    # 3. Criando a receita
    receita = Receita(nome="Bolo Simples", instrucoes="Misture tudo e asse.")

    # 4. Testando Adicionar e propriedades abstratas
    receita.adicionar_item(item1)
    receita.adicionar_item(item2)
    assert len(receita.itens) == 2
    assert item1 in receita.itens
    assert item1.coeficiente == 2.0

    # 5. Testando calcular_total do ItemReceita
    assert item1.calcular_total() == 8.0

    # 6. Testando Remover
    receita.remover_item(item1)
    assert len(receita.itens) == 1
    assert item1 not in receita.itens
    assert item2 in receita.itens


def test_remover_item_inexistente_levanta_erro():
    acucar = Ingrediente(nome="Açúcar", unidade="kg", quantidade=10, preco_base=4.0)
    item_da_receita = ItemReceita(insumo=acucar, coeficiente=1.0)
    item_perdido = ItemReceita(insumo=acucar, coeficiente=5.0)

    receita = Receita(nome="Café", instrucoes="Passe a água pelo filtro.")
    receita.adicionar_item(item_da_receita)

    # Deve levantar erro ao tentar remover um item que não foi adicionado a ela
    with pytest.raises(
        ValueError, match="O item informado não pertence a esta receita"
    ):
        receita.remover_item(item_perdido)
