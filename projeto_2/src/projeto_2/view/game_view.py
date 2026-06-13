import os

import pygame

from .base_view import BaseView
from .mapa_view import MapaView
from .menu_view import MenuView


class GameView(BaseView):
    def __init__(self, game_model_ro, largura: int = 800, altura: int = 600):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Campo Minado - Pygame")

        self.spritesheet = self._carregar_spritesheet()
        self.cor_fundo = (30, 30, 30)
        self.game_model_ro = game_model_ro

        # Sub-views
        largura_info = largura // 4
        self.mapa_view = MapaView(
            game_model_ro.mapa, self.spritesheet, tamanho_celula=32
        )
        self.menu_view = MenuView(
            game_model_ro.game_state, largura, altura, largura_info
        )

        # Definição das áreas (Layout)
        self.area_placar = (
            self.largura - largura_info,
            0,
            largura_info,
            self.altura // 10,
        )

    @property
    def offset(self) -> tuple[float, float]:
        return 0.0, 0.0

    @property
    def largura_info(self):
        return self.menu_view.largura_info

    @property
    def tamanho_celula(self):
        return self.mapa_view.tamanho_celula

    @property
    def offset_x(self):
        return self.mapa_view._offset_x

    @property
    def offset_y(self):
        return self.mapa_view._offset_y

    def calcular_offsets(self):
        """Delega o cálculo de offsets para a MapaView."""
        largura_area_mapa = self.largura - self.largura_info
        return self.mapa_view.calcular_offsets(largura_area_mapa, self.altura)

    def converter_tela_para_grade(self, pos):
        """Delega a conversão de coordenadas para a MapaView."""
        return self.mapa_view.converter_tela_para_grade(pos)

    def handle_event(self, event):
        """Delega o tratamento de eventos para as sub-views."""
        self.mapa_view.handle_event(event)
        self.menu_view.handle_event(event)

    def desenhar(self, tela: pygame.Surface):
        """Renderiza todos os componentes na tela."""
        self.mapa_view.desenhar(tela)
        self.menu_view.desenhar(tela)

    def render(self):
        """
        Executa o ciclo completo de renderização: limpar, desenhar e atualizar.
        """
        self.limpar_tela()
        self.desenhar(self.tela)
        self.atualizar()

    def _carregar_spritesheet(self):
        caminho_sprites = os.path.join("imagens", "New Piskel.png")
        try:
            return pygame.image.load(caminho_sprites).convert_alpha()
        except Exception:
            return pygame.Surface((32 * 20, 32))

    def limpar_tela(self):
        self.tela.fill(self.cor_fundo)

    def atualizar(self):
        pygame.display.flip()
