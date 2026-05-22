import pytest
from src.projeto_1.dominio.receita import Receita
from src.projeto_1.persistencia.receita import RepositorioReceita


def test_repositorio_receita_id_incremental_e_crud():
    repo = RepositorioReceita()

    # Criando receitas SEM ID
    rec1 = Receita(nome="Bolo de Fubá", instrucoes="Misture e asse.")
    rec2 = Receita(nome="Café coado", instrucoes="Passe a água quente.")

    # 1. Teste de ID Incremental (Save)
    repo.save(rec1)
    repo.save(rec2)

    assert rec1.id == 1
    assert rec2.id == 2

    # 2. Teste do Get
    assert repo.get(1) == rec1
    assert repo.get(2) == rec2

    # 3. Teste do List
    lista = repo.list()
    assert len(lista) == 2
    assert rec1 in lista
    assert rec2 in lista

    # 4. Teste do Update
    # Criamos uma nova instância representando a atualização da receita 1
    rec1_atualizada = Receita(
        nome="Bolo de Fubá Cremoso", instrucoes="Adicione queijo.", id=1
    )
    repo.update(rec1_atualizada)
    assert repo.get(1).nome == "Bolo de Fubá Cremoso"

    # 5. Teste do Delete
    repo.delete(1)
    assert repo.get(1) is None
    assert len(repo.list()) == 1


def test_repositorio_receita_erros_de_validacao():
    repo = RepositorioReceita()

    # Erro 1: Tentar salvar uma receita que o usuário já colocou ID manualmente
    rec_com_id_manual = Receita(
        nome="Pão de Queijo", instrucoes="Asse até dourar.", id=99
    )
    with pytest.raises(ValueError, match="ID já definido"):
        repo.save(rec_com_id_manual)

    # Erro 2: Tentar atualizar uma receita que nunca passou pelo save (sem ID)
    rec_sem_id = Receita(nome="Suco", instrucoes="Bata no liquidificador.")
    with pytest.raises(ValueError, match="sem ID"):
        repo.update(rec_sem_id)

    # Erro 3: Tentar atualizar um ID que tem número, mas não existe no repositório
    rec_fake = Receita(nome="Chá", instrucoes="Ferva a água.", id=999)
    with pytest.raises(ValueError, match="para atualizar"):
        repo.update(rec_fake)

    # Erro 4: Tentar deletar um ID inexistente
    with pytest.raises(ValueError, match="para remover"):
        repo.delete(888)
