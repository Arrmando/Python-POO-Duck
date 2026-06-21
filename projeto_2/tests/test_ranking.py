import os

import pytest

from projeto_2.persistencia.ranking_db import RepositorioRankingJSON


@pytest.fixture
def repo_temporario():
    """Cria um arquivo de testes temporário e o deleta depois dos testes."""
    arquivo_teste = "ranking_test.json"
    repo = RepositorioRankingJSON(caminho_arquivo=arquivo_teste)
    yield repo
    # Limpeza: apaga o arquivo de teste após rodar para não sujar o projeto
    if os.path.exists(arquivo_teste):
        os.remove(arquivo_teste)


def test_salvar_e_listar_ranking(repo_temporario):
    """Testa se o recorde é salvo e se o TOP 10 vem ordenado corretamente."""
    repo = repo_temporario

    # 1. Salva alguns recordes bagunçados (tempos diferentes)
    repo.salvar_pontuacao(nome="Gui", tempo=45, dificuldade="Médio")
    repo.salvar_pontuacao(nome="Pedro", tempo=30, dificuldade="Médio")
    repo.salvar_pontuacao(nome="Gabriel", tempo=60, dificuldade="Médio")
    repo.salvar_pontuacao(
        nome="Wallace", tempo=20, dificuldade="Fácil"
    )  # Dificuldade diferente

    # 2. Busca os melhores da dificuldade "Médio"
    melhores_medio = repo.listar_melhores("Médio")

    # 3. Validações (Asserts)
    assert len(melhores_medio) == 3  # Devem ter 3 registros no Médio

    # O menor tempo (30s do Pedro) deve vir em primeiro lugar!
    assert melhores_medio[0]["tempo_segundos"] == 30
    assert melhores_medio[0]["nome_jogador"] == "Pedro"

    # O maior tempo (60s do Gabriel) deve vir por último
    assert melhores_medio[-1]["tempo_segundos"] == 60


def test_limite_top_10(repo_temporario):
    """Garante que mesmo com 15 recordes, o repositório só retorna os 10 melhores."""
    repo = repo_temporario

    # Salva 12 recordes na mesma dificuldade
    for i in range(1, 13):
        repo.salvar_pontuacao(nome="Player", tempo=100 - i, dificuldade="Difícil")

    melhores_dificil = repo.listar_melhores("Difícil")

    # Deve cortar estritamente no 10
    assert len(melhores_dificil) == 10
