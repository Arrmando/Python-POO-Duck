import time


class GameState:
    def __init__(self):
        self._volume = 0.5
        self._dificuldade = "Medio"
        self._jogo_finalizado = False
        self._primeiro_clique = True
        self._qtd_bombas = 40

        # Timer state
        self._tempo_inicio = 0
        self._tempo_pausado = 0
        self._timer_rodando = False

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, valor):
        self._volume = valor

    @property
    def dificuldade(self):
        return self._dificuldade

    @dificuldade.setter
    def dificuldade(self, valor):
        self._dificuldade = valor

    @property
    def jogo_finalizado(self):
        return self._jogo_finalizado

    @jogo_finalizado.setter
    def jogo_finalizado(self, valor):
        self._jogo_finalizado = valor

    @property
    def primeiro_clique(self):
        return self._primeiro_clique

    @primeiro_clique.setter
    def primeiro_clique(self, valor):
        self._primeiro_clique = valor

    @property
    def qtd_bombas(self):
        return self._qtd_bombas

    @qtd_bombas.setter
    def qtd_bombas(self, valor):
        self._qtd_bombas = valor

    @property
    def tempo_segundos(self) -> int:
        if self._timer_rodando:
            return int(time.time() - self._tempo_inicio)
        return int(self._tempo_pausado)

    @property
    def tempo_formatado(self) -> str:
        total_segundos = self.tempo_segundos
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        return f"{minutos:02}:{segundos:02}"

    def iniciar_timer(self):
        if not self._timer_rodando:
            self._tempo_inicio = time.time() - self._tempo_pausado
            self._timer_rodando = True

    def parar_timer(self):
        if self._timer_rodando:
            self._tempo_pausado = time.time() - self._tempo_inicio
            self._timer_rodando = False

    def reiniciar_timer(self):
        self._tempo_inicio = 0
        self._tempo_pausado = 0
        self._timer_rodando = False
