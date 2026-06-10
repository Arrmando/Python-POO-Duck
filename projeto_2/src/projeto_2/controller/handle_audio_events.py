import pygame
import os


class HandleAudio:
    def __init__(self):
        pygame.mixer.init()
        self._musica_fundo = os.path.join("audio", "239539__dambient__8-bit-loop.mp3")
        self._volume_atual = 0.05

    def iniciar_musica_fundo(self):
        """Carrega e toca a música de fundo em loop."""
        try:
            if os.path.exists(self._musica_fundo):
                pygame.mixer.music.load(self._musica_fundo)
                pygame.mixer.music.set_volume(self._volume_atual)
                pygame.mixer.music.play(-1)
            else:
                print(f"Aviso: Arquivo de áudio não encontrado: {self._musica_fundo}")
        except pygame.error as e:
            print(f"Erro ao carregar áudio: {e}")

    def ajustar_volume(self, volume: float):
        """Ajusta o volume global da música (0.0 a 0.5)."""
        self._volume_atual = max(0.0, min(0.3, volume))
        pygame.mixer.music.set_volume(self._volume_atual)

    def processar_evento(self, evento):
        """Trata eventos globais de áudio, se necessário (ex: teclas de mute)."""
        pass
