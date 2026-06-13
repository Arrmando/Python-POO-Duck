from projeto_2.controller.tela_controller import TelaController
from projeto_2.model.game_state import GameState
from projeto_2.model.mapa_quadrado import MapaQuadrado
from projeto_2.view.janela import JanelaView


def run():
    largura, altura = 800, 600
    mapa = MapaQuadrado(18, 18)
    game_state = GameState()
    janela = JanelaView(mapa, game_state, largura, altura)
    controller = TelaController(janela, mapa, game_state)
    controller.run()


if __name__ == "__main__":
    run()
