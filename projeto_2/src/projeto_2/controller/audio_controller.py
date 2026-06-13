import os

import pygame

from projeto_2.constants import VOLUME_MAX


class AudioController:
    def __init__(self, game_state):
        pygame.mixer.init()
        self._game_state = game_state
        self._musica_fundo = os.path.join("audio", "239539__dambient__8-bit-loop.mp3")

    def iniciar_musica_fundo(self):
        """Carrega e toca a música de fundo em loop."""
        try:
            if os.path.exists(self._musica_fundo):
                pygame.mixer.music.load(self._musica_fundo)
                self.ajustar_volume(self._game_state.volume)
                pygame.mixer.music.play(-1)
            else:
                print(f"Aviso: Arquivo de áudio não encontrado: {self._musica_fundo}")
        except pygame.error as e:
            print(f"Erro ao carregar áudio: {e}")

    def ajustar_volume(self, volume: float):
        """Ajusta o volume global da música proporcionalmente ao VOLUME_MAX."""
        volume_final = volume * VOLUME_MAX
        pygame.mixer.music.set_volume(volume_final)

    def processar_evento(self, evento):
        pass
