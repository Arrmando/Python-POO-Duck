from projeto_2.controller.handle_mapa_events import HandleMapa

from projeto_2.model.bomba import Bomba
from projeto_2.model.mapa_quadrado import MapaQuadrado


def test_handle_mapa_obter_endereco_pela_posicao():
    """Garante que a conversão de pixels para grid está correta sem offset."""
    mapa = MapaQuadrado(10, 10)
    handler = HandleMapa(mapa)

    assert handler.obter_endereco_pela_posicao(0, 0) == (0, 0)
    assert handler.obter_endereco_pela_posicao(31, 31) == (0, 0)
    assert handler.obter_endereco_pela_posicao(32, 32) == (1, 1)


def test_handle_mapa_obter_endereco_com_offset():
    """A conversão de pixels para grid deve respeitar os offsets de centralização."""
    mapa = MapaQuadrado(10, 10)
    handler = HandleMapa(mapa)

    # Com offset de 100 pixels em cada eixo
    off_x, off_y = 100, 100

    # Clique em (100, 100) pixels -> (0, 0) grid
    assert handler.obter_endereco_pela_posicao(
        100, 100, offset_x=off_x, offset_y=off_y
    ) == (0, 0)

    # Clique em (131, 131) pixels -> (0, 0) grid
    assert handler.obter_endereco_pela_posicao(
        131, 131, offset_x=off_x, offset_y=off_y
    ) == (0, 0)

    # Clique em (132, 132) pixels -> (1, 1) grid
    assert handler.obter_endereco_pela_posicao(
        132, 132, offset_x=off_x, offset_y=off_y
    ) == (1, 1)


def test_handle_mapa_obter_sprite_numero():
    """Garante o mapeamento correto de valores para sprites."""
    handler = HandleMapa()
    # 0 -> 4*32
    assert handler.obter_sprite_numero(0) == 4 * 32
    # 1 -> 5*32
    assert handler.obter_sprite_numero(1) == 5 * 32
    # 8 -> 12*32
    assert handler.obter_sprite_numero(8) == 12 * 32


def test_handle_mapa_game_over():
    """Garante que atingir uma bomba finaliza o jogo e revela o mapa."""
    mapa = MapaQuadrado(3, 3)
    handler = HandleMapa(mapa)

    # Coloca uma bomba em (1,1)
    mapa.obter_celula(1, 1).adicionar_bomba(Bomba(1, False, 0))

    # Simula clique esquerdo em (1,1)
    # Mock de evento simplificado
    class MockEvento:
        def __init__(self, pos, button):
            self.pos = pos
            self.button = button

    # Desativa primeiro clique para facilitar (ou usa uma bomba conhecida)
    handler._primeiro_clique = False

    # Clique na bomba
    evento = MockEvento((1 * 32, 1 * 32), 1)
    handler.processar_evento(evento)

    assert handler._jogo_finalizado is True
    # Todas as células devem estar cavadas (status False)
    for linha in mapa.mapa:
        for celula in linha:
            assert celula.status is False

    # A bomba clicada deve estar explodida (sprite index 3)
    assert mapa.obter_celula(1, 1).obter_entidade(Bomba).sprite == 32 * 3
