import time


class HandlePlacar:
    def __init__(self):
        self._tempo_inicio = 0
        self._tempo_pausado = 0
        self._rodando = False

    def iniciar(self):
        """Inicia o cronômetro."""
        if not self._rodando:
            self._tempo_inicio = time.time() - self._tempo_pausado
            self._rodando = True

    def parar(self):
        """Para o cronômetro."""
        if self._rodando:
            self._tempo_pausado = time.time() - self._tempo_inicio
            self._rodando = False

    def reiniciar(self):
        """Zera o cronômetro."""
        self._tempo_inicio = 0
        self._tempo_pausado = 0
        self._rodando = False

    def obter_tempo_segundos(self) -> int:
        """Retorna o tempo decorrido em segundos."""
        if self._rodando:
            return int(time.time() - self._tempo_inicio)
        return int(self._tempo_pausado)

    def obter_tempo_formatado(self) -> str:
        """Retorna o tempo no formato MM:SS."""
        total_segundos = self.obter_tempo_segundos()
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        return f"{minutos:02}:{segundos:02}"

    def processar_evento(self, evento):
        # Por enquanto, o placar não processa eventos de clique
        pass
