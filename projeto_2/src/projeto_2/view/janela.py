import os

import pygame


class JanelaView:
    def __init__(self, largura: int = 800, altura: int = 600):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Campo Minado - Pygame")

        self.spritesheet = self._carregar_spritesheet()
        self.tamanho_celula = 32
        self.cor_fundo = (30, 30, 30)
        self.cor_painel = (50, 50, 50)
        self.cor_borda = (100, 100, 100)

        # Definição de Geometria da UI (Movido do Controller)
        self.largura_info = largura // 4
        self.btn_reiniciar_rect = pygame.Rect(620, 80, 160, 40)
        self.btn_placar_rect = pygame.Rect(620, 140, 160, 40)
        self.btn_facil_rect = pygame.Rect(620, 220, 160, 35)
        self.btn_medio_rect = pygame.Rect(620, 265, 160, 35)
        self.btn_dificil_rect = pygame.Rect(620, 310, 160, 35)

        self.slider_x_inicio = 630
        self.slider_x_fim = 770
        self.slider_y = 400
        self.knob_radius = 8

        self.offset_x = 0
        self.offset_y = 0

    def calcular_offsets(self, colunas, linhas):
        """Calcula a centralização do mapa baseado na grade."""
        largura_mapa = self.largura - self.largura_info
        self.offset_x = (largura_mapa - (colunas * self.tamanho_celula)) // 2
        self.offset_y = (self.altura - (linhas * self.tamanho_celula)) // 2
        return self.offset_x, self.offset_y

    def converter_tela_para_grade(self, pos):
        """Converte coordenadas da tela para (x, y) da grade."""
        px, py = pos
        gx = (px - self.offset_x) // self.tamanho_celula
        gy = (py - self.offset_y) // self.tamanho_celula
        return int(gx), int(gy)

    def obter_geometria(self):
        """Retorna os Rects e dimensões para o Controller processar eventos."""
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

    def _carregar_spritesheet(self):
        caminho_sprites = os.path.join("imagens", "New Piskel.png")
        try:
            return pygame.image.load(caminho_sprites).convert_alpha()
        except Exception:
            # Fallback em caso de erro no carregamento: superfície vazia
            return pygame.Surface((32 * 20, 32))

    def limpar_tela(self):
        self.tela.fill(self.cor_fundo)

    def atualizar(self):
        pygame.display.flip()

    def desenhar_layout_base(self, largura_info: int):
        """Desenha o painel lateral e as linhas divisórias."""
        # Fundo do painel lateral
        pygame.draw.rect(
            self.tela,
            self.cor_painel,
            (self.largura - largura_info, 0, largura_info, self.altura),
        )
        # Linhas divisórias
        pygame.draw.line(
            self.tela,
            self.cor_borda,
            (self.largura - largura_info, 0),
            (self.largura - largura_info, self.altura),
            2,
        )
        pygame.draw.line(
            self.tela,
            self.cor_borda,
            (self.largura - largura_info, (self.altura // 10)),
            (self.largura, self.altura // 10),
            2,
        )

    def desenhar_celulas(self, mapa, mapa_handler, offset_x: int, offset_y: int):
        """Exibe cada célula e seus sprites sobrepostos (números, bombas, bandeiras)."""
        for y in range(mapa.linhas):
            for x in range(mapa.colunas):
                celula = mapa.obter_celula(x, y)
                if not celula:
                    continue

                pos_tela = (
                    x * self.tamanho_celula + offset_x,
                    y * self.tamanho_celula + offset_y,
                )
                rect_base = pygame.Rect(
                    celula.sprite, 0, self.tamanho_celula, self.tamanho_celula
                )
                self.tela.blit(self.spritesheet, pos_tela, rect_base)

                sprites_extras = mapa_handler.obter_sprites_sobrepostos(celula)
                for sprite_x in sprites_extras:
                    rect_extra = pygame.Rect(
                        sprite_x, 0, self.tamanho_celula, self.tamanho_celula
                    )
                    self.tela.blit(self.spritesheet, pos_tela, rect_extra)

    def desenhar_placar(self, area, tempo_str):
        """Desenha o relógio na área do placar."""
        rect_placar = pygame.Rect(area)
        pygame.draw.rect(self.tela, (20, 20, 20), rect_placar)
        pygame.draw.rect(self.tela, (100, 100, 100), rect_placar, 1)

        fonte = pygame.font.SysFont("Consolas", 32, bold=True)
        texto = fonte.render(tempo_str, True, (255, 0, 0))
        texto_rect = texto.get_rect(center=rect_placar.center)
        self.tela.blit(texto, texto_rect)

    def desenhar_menu(self, menu_handler):
        """Desenha botões e o slider de volume."""
        fonte_p = pygame.font.SysFont("Arial", 24, bold=True)
        fonte_s = pygame.font.SysFont("Arial", 18, bold=True)

        COR_BTN = (150, 150, 150)
        COR_BTN_SEL = (100, 200, 100)
        COR_TEXTO = (30, 30, 30)

        # Botões REINICIAR e PLACAR
        pygame.draw.rect(self.tela, COR_BTN, self.btn_reiniciar_rect, border_radius=5)
        texto_r = fonte_p.render("REINICIAR", True, COR_TEXTO)
        self.tela.blit(
            texto_r, texto_r.get_rect(center=self.btn_reiniciar_rect.center)
        )

        pygame.draw.rect(self.tela, COR_BTN, self.btn_placar_rect, border_radius=5)
        texto_p = fonte_p.render("PLACAR", True, COR_TEXTO)
        self.tela.blit(
            texto_p, texto_p.get_rect(center=self.btn_placar_rect.center)
        )

        # Dificuldade
        label_fonte = pygame.font.SysFont("Arial", 20, bold=True)
        self.tela.blit(
            label_fonte.render("DIFICULDADE:", True, (200, 200, 200)), (620, 195)
        )

        botoes = [
            (self.btn_facil_rect, "FÁCIL", "Facil"),
            (self.btn_medio_rect, "MÉDIO", "Medio"),
            (self.btn_dificil_rect, "DIFÍCIL", "Dificil"),
        ]

        for rect, label_txt, id_dif in botoes:
            cor = COR_BTN_SEL if menu_handler.dificuldade_atual == id_dif else COR_BTN
            pygame.draw.rect(self.tela, cor, rect, border_radius=5)
            txt = fonte_s.render(label_txt, True, COR_TEXTO)
            self.tela.blit(txt, txt.get_rect(center=rect.center))

        # Volume
        self.tela.blit(label_fonte.render("VOLUME:", True, (200, 200, 200)), (620, 365))
        pygame.draw.line(
            self.tela,
            (100, 100, 100),
            (self.slider_x_inicio, self.slider_y),
            (self.slider_x_fim, self.slider_y),
            3,
        )
        knob_x = menu_handler.obter_knob_pos(self.slider_x_inicio, self.slider_x_fim)
        pygame.draw.circle(
            self.tela,
            (200, 200, 200),
            (knob_x, self.slider_y),
            self.knob_radius,
        )
        pygame.draw.circle(
            self.tela,
            (255, 255, 255),
            (knob_x, self.slider_y),
            self.knob_radius - 2,
        )
