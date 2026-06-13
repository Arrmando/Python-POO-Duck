import pygame

from projeto_2.constants import (
    DIFICULDADE_ALTERADA,
    PLACAR_CLICK,
    REINICIAR_CLICK,
    VOLUME_ALTERADO,
)
from projeto_2.utils import post_evento


class MenuView:
    def __init__(self, game_state_ro, largura: int, altura: int, largura_info: int):
        self.game_state_ro = game_state_ro
        self.largura = largura
        self.altura = altura
        self.largura_info = largura_info

        # Geometria da UI
        self.btn_reiniciar_rect = pygame.Rect(largura - largura_info + 20, 80, 160, 40)
        self.btn_placar_rect = pygame.Rect(largura - largura_info + 20, 140, 160, 40)
        self.btn_facil_rect = pygame.Rect(largura - largura_info + 20, 220, 160, 35)
        self.btn_medio_rect = pygame.Rect(largura - largura_info + 20, 265, 160, 35)
        self.btn_dificil_rect = pygame.Rect(largura - largura_info + 20, 310, 160, 35)

        self.slider_x_inicio = largura - largura_info + 30
        self.slider_x_fim = largura - 30
        self.slider_y = 400
        self.knob_radius = 8

        self.cor_painel = (50, 50, 50)
        self.cor_borda = (100, 100, 100)
        
        # Estado interno da View para interação
        self._arrastando_volume = False

    def obter_geometria(self):
        """Retorna os Rects e dimensões para o Controller."""
        return {
            "btn_reiniciar": self.btn_reiniciar_rect,
            "btn_placar": self.btn_placar_rect,
            "btn_facil": self.btn_facil_rect,
            "btn_medio": self.btn_medio_rect,
            "btn_dificil": self.btn_dificil_rect,
            "slider": {
                "x_inicio": self.slider_x_inicio,
                "x_fim": self.slider_x_fim,
                "y": self.slider_y,
                "knob_radius": self.knob_radius,
            },
        }

    def obter_knob_pos(self):
        """Calcula a posição X do círculo baseada no volume atual."""
        largura_total = self.slider_x_fim - self.slider_x_inicio
        return int(self.slider_x_inicio + (self.game_state_ro.volume * largura_total))

    def desenhar_layout_base(self, tela):
        """Desenha o painel lateral e as linhas divisórias."""
        pygame.draw.rect(
            tela,
            self.cor_painel,
            (self.largura - self.largura_info, 0, self.largura_info, self.altura),
        )
        pygame.draw.line(
            tela,
            self.cor_borda,
            (self.largura - self.largura_info, 0),
            (self.largura - self.largura_info, self.altura),
            2,
        )
        pygame.draw.line(
            tela,
            self.cor_borda,
            (self.largura - self.largura_info, (self.altura // 10)),
            (self.largura, self.altura // 10),
            2,
        )

    def _formatar_tempo(self) -> str:
        """Converte segundos do GameState para o formato MM:SS."""
        total_segundos = self.game_state_ro.tempo_segundos
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        return f"{minutos:02}:{segundos:02}"

    def desenhar_placar(self, tela, area):
        """Desenha o relógio na área do placar."""
        rect_placar = pygame.Rect(area)
        pygame.draw.rect(tela, (20, 20, 20), rect_placar)
        pygame.draw.rect(tela, (100, 100, 100), rect_placar, 1)

        texto_str = self._formatar_tempo()

        fonte = pygame.font.SysFont("Consolas", 32, bold=True)
        texto = fonte.render(texto_str, True, (255, 0, 0))
        texto_rect = texto.get_rect(center=rect_placar.center)
        tela.blit(texto, texto_rect)

    def handle_event(self, event):
        """Traduz eventos brutos do pygame em eventos de jogo."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # Botões
            if self.btn_reiniciar_rect.collidepoint(pos):
                post_evento(REINICIAR_CLICK)
            elif self.btn_placar_rect.collidepoint(pos):
                post_evento(PLACAR_CLICK)
            elif self.btn_facil_rect.collidepoint(pos):
                post_evento(DIFICULDADE_ALTERADA, nome='Facil', bombas=10)
            elif self.btn_medio_rect.collidepoint(pos):
                post_evento(DIFICULDADE_ALTERADA, nome='Medio', bombas=40)
            elif self.btn_dificil_rect.collidepoint(pos):
                post_evento(DIFICULDADE_ALTERADA, nome='Dificil', bombas=99)
            
            # Knob do Volume
            knob_x = self.obter_knob_pos()
            distancia = ((pos[0] - knob_x) ** 2 + (pos[1] - self.slider_y) ** 2) ** 0.5
            if distancia <= self.knob_radius + 5:
                self._arrastando_volume = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self._arrastando_volume = False

        elif event.type == pygame.MOUSEMOTION:
            if self._arrastando_volume:
                pos_x = event.pos[0]
                pos_x = max(self.slider_x_inicio, min(pos_x, self.slider_x_fim))
                largura_total = self.slider_x_fim - self.slider_x_inicio
                novo_volume = (pos_x - self.slider_x_inicio) / largura_total
                post_evento(VOLUME_ALTERADO, volume=novo_volume)

    def desenhar_menu(self, tela):
        """Desenha botões e o slider de volume."""
        fonte_p = pygame.font.SysFont("Arial", 24, bold=True)
        fonte_s = pygame.font.SysFont("Arial", 18, bold=True)

        COR_BTN = (150, 150, 150)
        COR_BTN_SEL = (100, 200, 100)
        COR_TEXTO = (30, 30, 30)

        # Botões REINICIAR e PLACAR
        pygame.draw.rect(tela, COR_BTN, self.btn_reiniciar_rect, border_radius=5)
        texto_r = fonte_p.render("REINICIAR", True, COR_TEXTO)
        tela.blit(texto_r, texto_r.get_rect(center=self.btn_reiniciar_rect.center))

        pygame.draw.rect(tela, COR_BTN, self.btn_placar_rect, border_radius=5)
        texto_p = fonte_p.render("PLACAR", True, COR_TEXTO)
        tela.blit(texto_p, texto_p.get_rect(center=self.btn_placar_rect.center))

        # Dificuldade
        label_fonte = pygame.font.SysFont("Arial", 20, bold=True)
        tela.blit(
            label_fonte.render("DIFICULDADE:", True, (200, 200, 200)),
            (self.largura - self.largura_info + 20, 195),
        )

        botoes = [
            (self.btn_facil_rect, "FÁCIL", "Facil"),
            (self.btn_medio_rect, "MÉDIO", "Medio"),
            (self.btn_dificil_rect, "DIFÍCIL", "Dificil"),
        ]

        for rect, label_txt, id_dif in botoes:
            cor = COR_BTN_SEL if self.game_state_ro.dificuldade == id_dif else COR_BTN
            pygame.draw.rect(tela, cor, rect, border_radius=5)
            txt = fonte_s.render(label_txt, True, COR_TEXTO)
            tela.blit(txt, txt.get_rect(center=rect.center))

        # Volume
        tela.blit(
            label_fonte.render("VOLUME:", True, (200, 200, 200)),
            (self.largura - self.largura_info + 20, 365),
        )
        pygame.draw.line(
            tela,
            (100, 100, 100),
            (self.slider_x_inicio, self.slider_y),
            (self.slider_x_fim, self.slider_y),
            3,
        )
        knob_x = self.obter_knob_pos()
        pygame.draw.circle(
            tela, (200, 200, 200), (knob_x, self.slider_y), self.knob_radius
        )
        pygame.draw.circle(
            tela, (255, 255, 255), (knob_x, self.slider_y), self.knob_radius - 2
        )
