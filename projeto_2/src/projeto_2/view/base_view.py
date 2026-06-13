from abc import ABC, abstractmethod

import pygame


class BaseView(ABC):
    """
    Classe base abstrata para todos os componentes visuais do jogo.
    Define a interface mínima para renderização e tratamento de eventos.
    """

    @property
    @abstractmethod
    def offset(self) -> tuple[float, float]:
        """
        Retorna o deslocamento (x, y) deste componente em relação à tela (ou ao pai).
        """
        pass

    @abstractmethod
    def desenhar(self, tela: pygame.Surface):
        """
        Renderiza o componente na superfície fornecida.
        """
        pass

    def handle_event(self, event: pygame.event.Event):
        """
        Processa eventos do Pygame. Implementação padrão não faz nada.
        """
        pass
