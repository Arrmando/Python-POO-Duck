import pytest
from src.projeto_1.dominio.ingrediente import Ingrediente
from src.projeto_1.dominio.homem_hora import HomemHora
from src.projeto_1.persistencia.insumo import RepositorioInsumo


def test_repositorio_id_incremental_e_crud():
    repo = RepositorioInsumo()

    # Criando ingredientes SEM ID (id padrão é None)
    ing1 = Ingrediente(nome="Açúcar", unidade="kg", quantidade=10, preco_base=4.0)
    ing2 = Ingrediente(nome="Farinha", unidade="kg", quantidade=5, preco_base=5.0)

    # 1. Teste de ID Incremental (Save)
    repo.save(ing1)
    repo.save(ing2)

    # O repositório deve ter injetado os IDs automaticamente na ordem correta
    assert ing1.id == 1
    assert ing2.id == 2

    # 2. Teste do Get
    assert repo.get(1) == ing1
    assert repo.get(2) == ing2

    # 3. Teste do List
    lista = repo.list()
    assert len(lista) == 2
    assert ing1 in lista
    assert ing2 in lista

    # 4. Teste do Update
    ing1.quantidade = 20
    repo.update(ing1)
    assert repo.get(1).quantidade == 20

    # 5. Teste do Delete
    repo.delete(1)
    assert repo.get(1) is None
    assert len(repo.list()) == 1


def test_repositorio_erros_de_validacao():
    repo = RepositorioInsumo()
    
    # Erro 1: Tentar salvar um objeto que o usuário já colocou ID manualmente
    ing_com_id_manual = Ingrediente(
        nome="Sal", unidade="un", quantidade=2, preco_base=1.5, id=99
    )
    with pytest.raises(ValueError, match="Não é possível salvar um insumo com ID já definido"):
        repo.save(ing_com_id_manual)
        
    # Erro 2: Tentar atualizar um objeto que nunca passou pelo save (não tem ID)
    ing_sem_id = Ingrediente(nome="Óleo", unidade="L", quantidade=1, preco_base=7.0)
    with pytest.raises(ValueError, match="Não é possível atualizar um insumo sem ID."):
        repo.update(ing_sem_id)
        
    # Erro 3: Tentar atualizar um ID que tem número, mas não existe no repositório
    ing_fake = Ingrediente(nome="Fermento", unidade="g", quantidade=1, preco_base=3.0)
    ing_fake._definir_id_persistencia(999)
    with pytest.raises(ValueError, match="para atualizar"):
        repo.update(ing_fake)

    # Erro 4: Tentar deletar um ID inexistente
    # AJUSTADO: Agora busca "remover", batendo com a mensagem real da sua classe
    with pytest.raises(ValueError, match="para remover"):
        repo.delete(888)


def test_repositorio_polimorfismo():
    repo = RepositorioInsumo()
    
    # Criamos um de cada tipo
    ingrediente = Ingrediente(nome="Chocolate", unidade="g", quantidade=500, preco_base=0.05)
    
    # AJUSTADO: Removido o argumento 'unidade' para respeitar o construtor do HomemHora
    homem_hora = HomemHora(nome="Confeiteiro", quantidade=4, preco_base=25.0)
    
    # O repositório deve aceitar ambos perfeitamente
    repo.save(ingrediente)
    repo.save(homem_hora)
    
    # Garante que ambos foram salvos e mantêm a ordem incremental
    assert len(repo.list()) == 2
    assert repo.get(1) == ingrediente
    assert repo.get(2) == homem_hora