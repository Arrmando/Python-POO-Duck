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
    def __init__(self, game_state_ro, largura: int, altura: int):
        """
        largura e altura referem-se às dimensões do PRÓPRIO menu.
        """
        self.game_state_ro = game_state_ro
        self.width = largura
        self.height = altura

        self.cor_painel = (50, 50, 50)
        self.cor_borda = (100, 100, 100)

        # Inicialização dos Widgets (coordenadas locais ao Menu)

        # 1. Background e Bordas
        self.bg_box = Box(rect=pygame.Rect(0, 0, largura, altura), cor=self.cor_painel)
        self.border_v = VerticalSeparator(
            x=0, y_inicio=0, y_fim=altura, cor=self.cor_borda
        )
        self.border_h = HorizontalSeparator(
            x_inicio=0, x_fim=largura, y=altura // 10, cor=self.cor_borda
        )

        # 2. Placar
        area_placar = pygame.Rect(0, 0, largura, altura // 10)
        self.placar_widget = PlacarWidget(rect=area_placar, game_state_ro=game_state_ro)

        # 3. Botões Principais
        self.btn_reiniciar = Button(
            rect=pygame.Rect(20, 80, 160, 40),
            texto="REINICIAR",
            evento_tipo=REINICIAR_CLICK,
        )
        self.btn_placar = Button(
            rect=pygame.Rect(20, 140, 160, 40), texto="PLACAR", evento_tipo=PLACAR_CLICK
        )

        # 4. Escolha de Dificuldade
        self.label_dificuldade = Text(
            pos=(20, 195), texto="DIFICULDADE:", cor=(200, 200, 200), tamanho=20
        )
        self.btns_dificuldade = [
            ChoiceButton(
                rect=pygame.Rect(20, 220, 160, 35),
                texto="FÁCIL",
                evento_tipo=DIFICULDADE_ALTERADA,
                id_escolha="Facil",
                game_state_ro=game_state_ro,
                nome="Facil",
                bombas=10,
            ),
            ChoiceButton(
                rect=pygame.Rect(20, 265, 160, 35),
                texto="MÉDIO",
                evento_tipo=DIFICULDADE_ALTERADA,
                id_escolha="Medio",
                game_state_ro=game_state_ro,
                nome="Medio",
                bombas=40,
            ),
            ChoiceButton(
                rect=pygame.Rect(20, 310, 160, 35),
                texto="DIFÍCIL",
                evento_tipo=DIFICULDADE_ALTERADA,
                id_escolha="Dificil",
                game_state_ro=game_state_ro,
                nome="Dificil",
                bombas=99,
            ),
        ]

        # 5. Slider de Volume
        self.slider_volume = SliderWidget(
            x_inicio=30,
            x_fim=largura - 30,
            y=400,
            label="VOLUME:",
            game_state_ro=game_state_ro,
        )

        # Lista de widgets para iteração
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

    def handle_event(self, event, offset: tuple[float, float] = (0, 0)):
        for widget in self.widgets:
            widget.handle_event(event, offset)

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        for widget in self.widgets:
            widget.desenhar(tela, offset)
