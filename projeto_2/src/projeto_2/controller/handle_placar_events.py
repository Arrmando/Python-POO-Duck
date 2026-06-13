class HandlePlacar:
    def __init__(self, game_state):
        self._game_state = game_state

    def iniciar(self):
        """Inicia o cronômetro."""
        self._game_state.iniciar_timer()

    def parar(self):
        """Para o cronômetro."""
        self._game_state.parar_timer()

    def reiniciar(self):
        """Zera o cronômetro."""
        self._game_state.reiniciar_timer()

    def obter_tempo_segundos(self) -> int:
        """Retorna o tempo decorrido em segundos."""
        return self._game_state.tempo_segundos

    def obter_tempo_formatado(self) -> str:
        """Retorna o tempo no formato MM:SS."""
        return self._game_state.tempo_formatado

    def processar_evento(self, evento):
        # Por enquanto, o placar não processa eventos de clique
        pass
