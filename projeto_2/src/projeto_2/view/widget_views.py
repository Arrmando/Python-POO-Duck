import pygame

from projeto_2.constants import VOLUME_ALTERADO
from projeto_2.utils import post_evento

from .base_view import BaseView


class Box(BaseView):
    def __init__(self, rect: pygame.Rect, cor: tuple[int, int, int]):
        self.rect = rect
        self.cor = cor

    @property
    def offset(self) -> tuple[float, float]:
        return float(self.rect.x), float(self.rect.y)

    def desenhar(self, tela: pygame.Surface):
        pygame.draw.rect(tela, self.cor, self.rect)


class HorizontalSeparator(BaseView):
    def __init__(
        self,
        x_inicio: int,
        x_fim: int,
        y: int,
        cor: tuple[int, int, int],
        largura: int = 2,
    ):
        self.x_inicio = x_inicio
        self.x_fim = x_fim
        self.y = y
        self.cor = cor
        self.largura = largura

    @property
    def offset(self) -> tuple[float, float]:
        return float(self.x_inicio), float(self.y)

    def desenhar(self, tela: pygame.Surface):
        pygame.draw.line(
            tela, self.cor, (self.x_inicio, self.y), (self.x_fim, self.y), self.largura
        )


class VerticalSeparator(BaseView):
    def __init__(
        self,
        x: int,
        y_inicio: int,
        y_fim: int,
        cor: tuple[int, int, int],
        largura: int = 2,
    ):
        self.x = x
        self.y_inicio = y_inicio
        self.y_fim = y_fim
        self.cor = cor
        self.largura = largura

    @property
    def offset(self) -> tuple[float, float]:
        return float(self.x), float(self.y_inicio)

    def desenhar(self, tela: pygame.Surface):
        pygame.draw.line(
            tela, self.cor, (self.x, self.y_inicio), (self.x, self.y_fim), self.largura
        )


class Text(BaseView):
    def __init__(
        self,
        pos: tuple[int, int],
        texto: str,
        cor: tuple[int, int, int],
        tamanho: int = 20,
        bold: bool = True,
        fonte_nome: str = "Arial",
        centralizar_em_rect: pygame.Rect = None,
    ):
        self.pos = pos
        self.texto = texto
        self.cor = cor
        self.fonte = pygame.font.SysFont(fonte_nome, tamanho, bold=bold)
        self.centralizar_em_rect = centralizar_em_rect

    @property
    def offset(self) -> tuple[float, float]:
        return float(self.pos[0]), float(self.pos[1])

    def desenhar(self, tela: pygame.Surface):
        txt_surf = self.fonte.render(self.texto, True, self.cor)
        if self.centralizar_em_rect:
            txt_rect = txt_surf.get_rect(center=self.centralizar_em_rect.center)
            tela.blit(txt_surf, txt_rect)
        else:
            tela.blit(txt_surf, self.pos)


class Button(BaseView):
    def __init__(self, rect: pygame.Rect, texto: str, evento_tipo: int, **evento_data):
        self.rect = rect
        self.cor_fundo = (150, 150, 150)
        self.evento_tipo = evento_tipo
        self.evento_data = evento_data

        # Usa o widget Text internamente
        self.text_widget = Text(
            (0, 0),
            texto,
            (30, 30, 30),
            tamanho=24,
            bold=True,
            centralizar_em_rect=self.rect,
        )

    @property
    def offset(self) -> tuple[float, float]:
        return float(self.rect.x), float(self.rect.y)

    def desenhar(self, tela: pygame.Surface):
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=5)
        self.text_widget.desenhar(tela)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                post_evento(self.evento_tipo, **self.evento_data)


class ChoiceButton(Button):
    def __init__(
        self,
        rect: pygame.Rect,
        texto: str,
        evento_tipo: int,
        id_escolha: str,
        game_state_ro,
        **evento_data,
    ):
        super().__init__(rect, texto, evento_tipo, **evento_data)
        self.id_escolha = id_escolha
        self.game_state_ro = game_state_ro
        self.cor_sel = (100, 200, 100)

        # Ajusta o tamanho da fonte para ChoiceButton
        self.text_widget.fonte = pygame.font.SysFont("Arial", 18, bold=True)

    def desenhar(self, tela: pygame.Surface):
        selecionado = self.game_state_ro.dificuldade == self.id_escolha
        cor = self.cor_sel if selecionado else self.cor_fundo

        pygame.draw.rect(tela, cor, self.rect, border_radius=5)
        self.text_widget.desenhar(tela)


class SliderWidget(BaseView):
    def __init__(self, x_inicio, x_fim, y, label, game_state_ro):
        self.x_inicio = x_inicio
        self.x_fim = x_fim
        self.y = y
        self.game_state_ro = game_state_ro
        self.knob_radius = 8
        self._arrastando = False

        # Usa o widget Text para o label
        self.label_widget = Text((x_inicio, y - 35), label, (200, 200, 200), tamanho=20)

    @property
    def offset(self) -> tuple[float, float]:
        return float(self.x_inicio), float(self.y)

    def _obter_knob_pos(self):
        largura_total = self.x_fim - self.x_inicio
        return int(self.x_inicio + (self.game_state_ro.volume * largura_total))

    def desenhar(self, tela: pygame.Surface):
        self.label_widget.desenhar(tela)

        # Linha do slider
        pygame.draw.line(
            tela, (100, 100, 100), (self.x_inicio, self.y), (self.x_fim, self.y), 3
        )

        # Knob
        knob_x = self._obter_knob_pos()
        pygame.draw.circle(tela, (200, 200, 200), (knob_x, self.y), self.knob_radius)
        pygame.draw.circle(
            tela, (255, 255, 255), (knob_x, self.y), self.knob_radius - 2
        )

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            knob_x = self._obter_knob_pos()
            dist = ((event.pos[0] - knob_x) ** 2 + (event.pos[1] - self.y) ** 2) ** 0.5
            if dist <= self.knob_radius + 5:
                self._arrastando = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self._arrastando = False
        elif event.type == pygame.MOUSEMOTION and self._arrastando:
            pos_x = max(self.x_inicio, min(event.pos[0], self.x_fim))
            novo_vol = (pos_x - self.x_inicio) / (self.x_fim - self.x_inicio)
            post_evento(VOLUME_ALTERADO, volume=novo_vol)


class PlacarWidget(BaseView):
    def __init__(self, rect: pygame.Rect, game_state_ro):
        self.rect = rect
        self.game_state_ro = game_state_ro

        # Usa o widget Text para o tempo
        self.text_widget = Text(
            (0, 0),
            "00:00",
            (255, 0, 0),
            tamanho=32,
            bold=True,
            fonte_nome="Consolas",
            centralizar_em_rect=self.rect,
        )

    @property
    def offset(self) -> tuple[float, float]:
        return float(self.rect.x), float(self.rect.y)

    def _formatar_tempo(self) -> str:
        total_segundos = self.game_state_ro.tempo_segundos
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        return f"{minutos:02}:{segundos:02}"

    def desenhar(self, tela: pygame.Surface):
        # Fundo do placar
        pygame.draw.rect(tela, (20, 20, 20), self.rect)
        pygame.draw.rect(tela, (100, 100, 100), self.rect, 1)

        # Atualiza o texto do widget antes de desenhar
        self.text_widget.texto = self._formatar_tempo()
        self.text_widget.desenhar(tela)
