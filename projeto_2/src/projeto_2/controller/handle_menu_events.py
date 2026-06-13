import pygame


class HandleMenu:
    def __init__(self, game_state):
        self._game_state = game_state

    @property
    def volume(self):
        return self._game_state.volume

    @volume.setter
    def volume(self, valor):
        self._game_state.volume = valor

    @property
    def dificuldade_atual(self):
        return self._game_state.dificuldade

    @dificuldade_atual.setter
    def dificuldade_atual(self, valor):
        self._game_state.dificuldade = valor

    def obter_knob_pos(self, slider_x_inicio=630, slider_x_fim=770):
        """Calcula a posição X do círculo baseada no volume atual."""
        largura_total = slider_x_fim - slider_x_inicio
        return int(slider_x_inicio + (self.volume * largura_total))
