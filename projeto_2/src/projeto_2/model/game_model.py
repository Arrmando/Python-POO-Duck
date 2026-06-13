class GameModel:
    def __init__(self, mapa, game_state):
        self.mapa = mapa
        self.game_state = game_state

    def iniciar_jogo(self):
        """Inicializa o mapa e reseta o estado do jogo."""
        self.mapa.reset()
        self.game_state.primeiro_clique = True
        self.game_state.jogo_finalizado = False
        self.game_state.reiniciar_timer()
        return self.mapa
