import pytest
from src.projeto_1.dominio.ingrediente import Ingrediente
from src.projeto_1.dominio.receita import ItemReceita, Receita


def test_criar_receita_e_manipular_itens():
    # 1. Criando os insumos bases para o teste
    acucar = Ingrediente(nome="Açúcar", unidade="kg", quantidade=10, preco_base=4.0)
    farinha = Ingrediente(nome="Farinha", unidade="kg", quantidade=5, preco_base=5.0)

    # 2. Criando os itens da receita
    item1 = ItemReceita(insumo=acucar, coeficiente=2.0)  # Total: 8.0
    item2 = ItemReceita(insumo=farinha, coeficiente=3.0)  # Total: 15.0

    # 3. Criando a receita
    receita = Receita(nome="Bolo Simples", instrucoes="Misture tudo e asse.")

    # 4. Adicionando os itens
    receita.adicionar_item(item1)
    receita.adicionar_item(item2)

    assert len(receita.itens) == 2
    assert item1 in receita.itens
    assert item1.coeficiente == 2.0

    # 5. TESTE DA REVISÃO: Verifica se calcula o preço composto total somado
    # 8.0 (item1) + 15.0 (item2) = 23.0
    assert receita.calcular_total() == 23.0

    # 6. Testando Remover e recalculando o total
    receita.remover_item(item1)
    assert len(receita.itens) == 1
    assert receita.calcular_total() == 15.0  # Sobrou apenas a farinha


def test_remover_item_inexistente_levanta_erro():
    acucar = Ingrediente(nome="Açúcar", unidade="kg", quantidade=10, preco_base=4.0)
    item_da_receita = ItemReceita(insumo=acucar, coeficiente=1.0)
    item_perdido = ItemReceita(insumo=acucar, coeficiente=5.0)

    receita = Receita(nome="Café", instrucoes="Passe a água pelo filtro.")
    receita.adicionar_item(item_da_receita)

    with pytest.raises(
        ValueError, match="O item informado não pertence a esta receita"
    ):
        receita.remover_item(item_perdido)
