import os
import sys

import pygame

from projeto_2.controller.tela_controller import TelaController


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

    def desenhar_celulas(self, mapa, controller, offset_x: int, offset_y: int):
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

                sprites_extras = controller.handle_mapa.obter_sprites_sobrepostos(
                    celula
                )
                for sprite_x in sprites_extras:
                    rect_extra = pygame.Rect(
                        sprite_x, 0, self.tamanho_celula, self.tamanho_celula
                    )
                    self.tela.blit(self.spritesheet, pos_tela, rect_extra)

    def desenhar_placar(self, controller):
        """Desenha o relógio na área do placar."""
        area = controller.area_placar
        rect_placar = pygame.Rect(area)
        pygame.draw.rect(self.tela, (20, 20, 20), rect_placar)
        pygame.draw.rect(self.tela, (100, 100, 100), rect_placar, 1)

        tempo_str = controller.handle_placar.obter_tempo_formatado()
        fonte = pygame.font.SysFont("Consolas", 32, bold=True)
        texto = fonte.render(tempo_str, True, (255, 0, 0))
        texto_rect = texto.get_rect(center=rect_placar.center)
        self.tela.blit(texto, texto_rect)

    def desenhar_menu(self, controller):
        """Desenha botões e o slider de volume."""
        fonte_p = pygame.font.SysFont("Arial", 24, bold=True)
        fonte_s = pygame.font.SysFont("Arial", 18, bold=True)

        COR_BTN = (150, 150, 150)
        COR_BTN_SEL = (100, 200, 100)
        COR_TEXTO = (30, 30, 30)

        h_menu = controller.handle_menu

        # Botões REINICIAR e PLACAR
        pygame.draw.rect(self.tela, COR_BTN, h_menu.btn_reiniciar_rect, border_radius=5)
        texto_r = fonte_p.render("REINICIAR", True, COR_TEXTO)
        self.tela.blit(
            texto_r, texto_r.get_rect(center=h_menu.btn_reiniciar_rect.center)
        )

        pygame.draw.rect(self.tela, COR_BTN, h_menu.btn_placar_rect, border_radius=5)
        texto_p = fonte_p.render("PLACAR", True, COR_TEXTO)
        self.tela.blit(texto_p, texto_p.get_rect(center=h_menu.btn_placar_rect.center))

        # Dificuldade
        label_fonte = pygame.font.SysFont("Arial", 20, bold=True)
        self.tela.blit(
            label_fonte.render("DIFICULDADE:", True, (200, 200, 200)), (620, 195)
        )

        botoes = [
            (h_menu.btn_facil_rect, "FÁCIL", "Facil"),
            (h_menu.btn_medio_rect, "MÉDIO", "Medio"),
            (h_menu.btn_dificil_rect, "DIFÍCIL", "Dificil"),
        ]

        for rect, label_txt, id_dif in botoes:
            cor = COR_BTN_SEL if h_menu.dificuldade_atual == id_dif else COR_BTN
            pygame.draw.rect(self.tela, cor, rect, border_radius=5)
            txt = fonte_s.render(label_txt, True, COR_TEXTO)
            self.tela.blit(txt, txt.get_rect(center=rect.center))

        # Volume
        self.tela.blit(label_fonte.render("VOLUME:", True, (200, 200, 200)), (620, 365))
        pygame.draw.line(
            self.tela,
            (100, 100, 100),
            (h_menu.slider_x_inicio, h_menu.slider_y),
            (h_menu.slider_x_fim, h_menu.slider_y),
            3,
        )
        knob_x = h_menu.obter_knob_pos()
        pygame.draw.circle(
            self.tela, (200, 200, 200), (knob_x, h_menu.slider_y), h_menu.knob_radius
        )
        pygame.draw.circle(
            self.tela,
            (255, 255, 255),
            (knob_x, h_menu.slider_y),
            h_menu.knob_radius - 2,
        )


def criar_janela():
    largura, altura = 800, 600
    janela = JanelaView(largura, altura)

    controller = TelaController(largura, altura)
    mapa = controller.inicializar_mapa(18, 18)

    # Inicia a música através do Handler de Áudio
    controller.handle_audio.iniciar_musica_fundo()

    largura_info = largura // 4
    offset_x = ((largura - largura_info) - (mapa.colunas * janela.tamanho_celula)) // 2
    offset_y = (altura - (mapa.linhas * janela.tamanho_celula)) // 2

    rodando = True
    while rodando:
        mapa = controller.handle_mapa._mapa
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            controller.tratar_evento(evento, offset_x=offset_x, offset_y=offset_y)

        janela.limpar_tela()
        janela.desenhar_celulas(mapa, controller, offset_x, offset_y)
        janela.desenhar_layout_base(largura_info)
        janela.desenhar_placar(controller)
        janela.desenhar_menu(controller)
        janela.atualizar()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    criar_janela()
