import pygame

from projeto_2.constants import (
    DIFICULDADE_ALTERADA,
    PLACAR_CLICK,
    REINICIAR_CLICK,
)

from .base_view import BaseView
from .widget_views import (
    Box,
    Button,
    ChoiceButton,
    HorizontalSeparator,
    PlacarWidget,
    SliderWidget,
    Text,
    VerticalSeparator,
)


class MenuView(BaseView):
    def __init__(self, game_state_ro, largura: int, altura: int, largura_info: int):
        self.game_state_ro = game_state_ro
        self.largura = largura
        self.altura = altura
        self.largura_info = largura_info

        self.cor_painel = (50, 50, 50)
        self.cor_borda = (100, 100, 100)

        # Inicialização dos Widgets
        ox = largura - largura_info

        # 1. Background e Bordas
        self.bg_box = Box(pygame.Rect(ox, 0, largura_info, altura), self.cor_painel)
        self.border_v = VerticalSeparator(ox, 0, altura, self.cor_borda)
        self.border_h = HorizontalSeparator(ox, largura, altura // 10, self.cor_borda)

        # 2. Placar
        area_placar = pygame.Rect(ox, 0, largura_info, altura // 10)
        self.placar_widget = PlacarWidget(area_placar, game_state_ro)

        # 3. Botões Principais
        self.btn_reiniciar = Button(
            pygame.Rect(ox + 20, 80, 160, 40), "REINICIAR", REINICIAR_CLICK
        )
        self.btn_placar = Button(
            pygame.Rect(ox + 20, 140, 160, 40), "PLACAR", PLACAR_CLICK
        )

        # 4. Escolha de Dificuldade
        self.label_dificuldade = Text(
            (ox + 20, 195), "DIFICULDADE:", (200, 200, 200), tamanho=20
        )
        self.btns_dificuldade = [
            ChoiceButton(
                pygame.Rect(ox + 20, 220, 160, 35),
                "FÁCIL",
                DIFICULDADE_ALTERADA,
                "Facil",
                game_state_ro,
                nome="Facil",
                bombas=10,
            ),
            ChoiceButton(
                pygame.Rect(ox + 20, 265, 160, 35),
                "MÉDIO",
                DIFICULDADE_ALTERADA,
                "Medio",
                game_state_ro,
                nome="Medio",
                bombas=40,
            ),
            ChoiceButton(
                pygame.Rect(ox + 20, 310, 160, 35),
                "DIFÍCIL",
                DIFICULDADE_ALTERADA,
                "Dificil",
                game_state_ro,
                nome="Dificil",
                bombas=99,
            ),
        ]

        # 5. Slider de Volume
        self.slider_volume = SliderWidget(
            ox + 30, largura - 30, 400, "VOLUME:", game_state_ro
        )

        # Lista de widgets para iteração (desenho e eventos)
        self.widgets = [
            self.bg_box,
            self.border_v,
            self.border_h,
            self.placar_widget,
            self.btn_reiniciar,
            self.btn_placar,
            self.label_dificuldade,
            *self.btns_dificuldade,
            self.slider_volume,
        ]

    @property
    def offset(self) -> tuple[float, float]:
        return float(self.largura - self.largura_info), 0.0

    def handle_event(self, event):
        for widget in self.widgets:
            widget.handle_event(event)

    def desenhar(self, tela: pygame.Surface):
        for widget in self.widgets:
            widget.desenhar(tela)
