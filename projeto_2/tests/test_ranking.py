import os
import pytest

from projeto_2.persistencia.ranking_db import RepositorioRankingJSON


@pytest.fixture
def repo_teste():
    """Fixture que cria um arquivo de ranking de testes e o deleta depois."""
    nome_arquivo = "ranking_teste.json"
    repo = RepositorioRankingJSON(caminho_arquivo=nome_arquivo)
    yield repo
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)


def test_deve_salvar_e_ordenar_ranking_por_menor_tempo(repo_teste):
    repo_teste.salvar_pontuacao(nome="Gui", tempo=50, dificuldade="Fácil")
    repo_teste.salvar_pontuacao(nome="Pedro", tempo=30, dificuldade="Fácil")
    repo_teste.salvar_pontuacao(nome="Wallace", tempo=45, dificuldade="Fácil")
    repo_teste.salvar_pontuacao(nome="Daniel", tempo=20, dificuldade="Médio")

    melhores_facil = repo_teste.listar_melhores(dificuldade="Fácil")

    assert len(melhores_facil) == 3
    assert melhores_facil[0]["nome_jogador"] == "Pedro"
    assert melhores_facil[1]["nome_jogador"] == "Wallace"
    assert melhores_facil[2]["nome_jogador"] == "Gui"