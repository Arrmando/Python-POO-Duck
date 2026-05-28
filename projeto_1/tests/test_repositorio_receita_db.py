import pytest
from src.projeto_1.dominio.ingrediente import Ingrediente
from src.projeto_1.dominio.receita import ItemReceita, Receita
from src.projeto_1.persistencia.insumo import RepositorioInsumo
from src.projeto_1.persistencia.receita import RepositorioReceitaDB


@pytest.fixture
def repo_insumo_mock():
    """Gera um repositório de insumos em memória povoado para servir de suporte."""
    repo = RepositorioInsumo()
    acucar = Ingrediente(nome="Açúcar", unidade="kg", quantidade=10, preco_base=4.0)
    repo.save(acucar)  # ID 1
    return repo


@pytest.fixture
def repo_receita_db(tmp_path, repo_insumo_mock):
    """Gera um repositório de receitas JSON isolado."""
    arquivo_json = tmp_path / "receitas_teste.json"
    return RepositorioReceitaDB(path=arquivo_json, repo_insumo=repo_insumo_mock)


def test_receita_db_crud_completo(repo_receita_db, repo_insumo_mock):
    insumo = repo_insumo_mock.get(1)
    item = ItemReceita(insumo=insumo, coeficiente=2.0)

    rec = Receita(nome="Suco Doce", instrucoes="Misture açúcar e água.")
    rec.adicionar_item(item)

    # 1. Testando Save
    repo_receita_db.save(rec)

    salva = repo_receita_db.get(1)
    assert salva.id == 1
    assert salva.nome == "Suco Doce"
    assert len(salva.itens) == 1
    assert salva.itens[0].insumo.nome == "Açúcar"

    # 2. Testando Update
    rec_atualizada = Receita(nome="Suco Ultra Doce", instrucoes="Muito açúcar.", id=1)
    repo_receita_db.update(rec_atualizada)
    assert repo_receita_db.get(1).nome == "Suco Ultra Doce"

    # 3. Testando Delete
    repo_receita_db.delete(1)
    assert repo_receita_db.get(1) is None


def test_receita_db_persistência_entre_chamadas(tmp_path, repo_insumo_mock):
    """Garanta que os IDs e dados continuam lá mesmo fechando o programa."""
    arquivo_json = tmp_path / "receitas_reais.json"

    # Primeira execução salva
    repo1 = RepositorioReceitaDB(path=arquivo_json, repo_insumo=repo_insumo_mock)
    rec1 = Receita(nome="Água com açúcar", instrucoes="Mexa bem.")
    repo1.save(rec1)

    # Segunda execução abre o mesmo arquivo
    repo2 = RepositorioReceitaDB(path=arquivo_json, repo_insumo=repo_insumo_mock)
    rec2 = Receita(nome="Café", instrucoes="Passe o café.")
    repo2.save(rec2)

    # O segundo ID deve obrigatoriamente ser incremental (2)
    assert repo2.get(2).nome == "Café"
    assert repo2.get(1).nome == "Água com açúcar"
