from src.projeto_1.dominio.ingrediente import Ingrediente
from src.projeto_1.persistencia.insumo import RepositorioInsumo


def test_repositorio_crud_e_polimorfismo():
    repo = RepositorioInsumo()

    # 1. Criando instâncias (Testando com Ingrediente)
    ingrediente = Ingrediente(
        nome="Açúcar", unidade="kg", quantidade=10, preco_base=4.0, id=1
    )

    # 2. Teste do Save e Get
    repo.save(ingrediente)
    assert repo.get(1) == ingrediente

    # 3. Teste do List
    assert len(repo.list()) == 1
    assert ingrediente in repo.list()

    # 4. Teste do Update
    ingrediente.quantidade = 15
    repo.update(ingrediente)
    assert repo.get(1).quantidade == 15

    # 5. Teste do Delete
    repo.delete(1)
    assert repo.get(1) is None
    assert len(repo.list()) == 0
