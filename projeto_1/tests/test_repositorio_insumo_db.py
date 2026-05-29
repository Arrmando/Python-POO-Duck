import pytest
from src.projeto_1.dominio.homem_hora import HomemHora
from src.projeto_1.dominio.ingrediente import Ingrediente
from src.projeto_1.persistencia.insumo import RepositorioInsumoDB


@pytest.fixture
def repo_db(tmp_path):
    """Gera um repositório JSON isolado dentro de uma pasta temporária do pytest."""
    arquivo_json = tmp_path / "insumos_teste.json"
    return RepositorioInsumoDB(path=arquivo_json)


def test_db_id_incremental_e_crud_completo(repo_db):
    ing = Ingrediente(nome="Açúcar", unidade="kg", quantidade=10, preco_base=4.0)
    hh = HomemHora(nome="Confeiteiro", quantidade=5, preco_base=20.0)

    # 1. Testando o Save e persistência inicial
    repo_db.save(ing)
    repo_db.save(hh)

    # Coletas do banco de dados simulado
    salvo1 = repo_db.get(1)
    salvo2 = repo_db.get(2)

    assert salvo1.id == 1
    assert salvo1.nome == "Açúcar"
    assert salvo2.id == 2
    assert salvo2.nome == "Confeiteiro"

    # 2. Testando List
    lista = repo_db.list()
    assert len(lista) == 2

    # 3. Testando o Update
    salvo1.quantidade = 99
    repo_db.update(salvo1)
    assert repo_db.get(1).quantidade == 99

    # 4. Testando Delete
    repo_db.delete(1)
    assert repo_db.get(1) is None
    assert len(repo_db.list()) == 1


def test_db_gerenciamento_de_ids_entre_chamadas_diferentes(tmp_path):
    """Teste crucial solicitado pelo Pedro: Garante que se o repositório fechar

    e abrir outro apontando pro mesmo arquivo, o ID continua de onde parou.
    """
    arquivo_json = tmp_path / "insumos_persistidos.json"

    # Instância 1: Salva o primeiro item
    repo1 = RepositorioInsumoDB(path=arquivo_json)
    ing1 = Ingrediente(nome="Sal", unidade="g", quantidade=100, preco_base=0.1)
    repo1.save(ing1)

    # Instância 2: Abre o mesmo arquivo simulando uma nova execução do sistema
    repo2 = RepositorioInsumoDB(path=arquivo_json)
    ing2 = Ingrediente(nome="Óleo", unidade="L", quantidade=1, preco_base=7.0)
    repo2.save(ing2)

    # O segundo item DEVE receber o ID 2, pois o arquivo JSON guardou o estado anterior
    assert repo2.get(2).nome == "Óleo"
    assert repo2.get(1).nome == "Sal"


def test_db_erros_de_validacao(repo_db):
    # Tentar salvar com ID manual direto no banco de dados deve gerar erro
    ing_com_id = Ingrediente(
        nome="Fermento", unidade="g", quantidade=1, preco_base=2.0, id=55
    )
    with pytest.raises(ValueError, match="ID já definido"):
        repo_db.save(ing_com_id)

    # Tentar remover ID inexistente no arquivo
    with pytest.raises(ValueError, match="para remover"):
        repo_db.delete(999)
