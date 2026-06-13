from abc import ABC, abstractmethod
import pygame


class BaseView(ABC):
    """
    Classe base abstrata para todos os componentes visuais do jogo.
    Define a interface mínima para renderização e tratamento de eventos
    suportando posicionamento dinâmico via offsets.
    """

    @abstractmethod
    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        """
        Renderiza o componente na superfície fornecida, aplicando o offset.
        """
        pass

    def handle_event(self, event: pygame.event.Event, offset: tuple[float, float] = (0, 0)):
        """
        Processa eventos do Pygame considerando o offset absoluto do componente.
        """
        pass
