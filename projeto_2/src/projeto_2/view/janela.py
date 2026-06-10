import pygame
import sys
import os
from projeto_2.controller.tela_controller import TelaController


def desenhar_celulas(tela, spritesheet, mapa, controller, tamanho_celula, offset_x, offset_y):
    """Exibe cada célula e seus sprites sobrepostos (números, bombas, bandeiras)."""
    for y in range(mapa.linhas):
        for x in range(mapa.colunas):
            celula = mapa.obter_celula(x, y)
            if not celula:
                continue

            pos_tela = (x * tamanho_celula + offset_x, y * tamanho_celula + offset_y)
            rect_base = pygame.Rect(celula.sprite, 0, tamanho_celula, tamanho_celula)
            tela.blit(spritesheet, pos_tela, rect_base)

            sprites_extras = controller.handle_mapa.obter_sprites_sobrepostos(celula)
            for sprite_x in sprites_extras:
                rect_extra = pygame.Rect(sprite_x, 0, tamanho_celula, tamanho_celula)
                tela.blit(spritesheet, pos_tela, rect_extra)


def desenhar_placar(tela, controller):
    """Desenha o relógio na área do placar."""
    area = controller.area_placar
    rect_placar = pygame.Rect(area)
    pygame.draw.rect(tela, (20, 20, 20), rect_placar)
    pygame.draw.rect(tela, (100, 100, 100), rect_placar, 1)

    tempo_str = controller.handle_placar.obter_tempo_formatado()
    fonte = pygame.font.SysFont("Consolas", 32, bold=True)
    texto = fonte.render(tempo_str, True, (255, 0, 0))
    texto_rect = texto.get_rect(center=rect_placar.center)
    tela.blit(texto, texto_rect)


def desenhar_menu(tela, controller):
    """Desenha botões e o slider de volume."""
    fonte_p = pygame.font.SysFont("Arial", 24, bold=True)
    fonte_s = pygame.font.SysFont("Arial", 18, bold=True)
    
    COR_BTN = (150, 150, 150)
    COR_BTN_SEL = (100, 200, 100)
    COR_TEXTO = (30, 30, 30)

    h_menu = controller.handle_menu

    # Botões REINICIAR e PLACAR
    pygame.draw.rect(tela, COR_BTN, h_menu.btn_reiniciar_rect, border_radius=5)
    texto_r = fonte_p.render("REINICIAR", True, COR_TEXTO)
    tela.blit(texto_r, texto_r.get_rect(center=h_menu.btn_reiniciar_rect.center))

    pygame.draw.rect(tela, COR_BTN, h_menu.btn_placar_rect, border_radius=5)
    texto_p = fonte_p.render("PLACAR", True, COR_TEXTO)
    tela.blit(texto_p, texto_p.get_rect(center=h_menu.btn_placar_rect.center))

    # Dificuldade
    label_fonte = pygame.font.SysFont("Arial", 20, bold=True)
    tela.blit(label_fonte.render("DIFICULDADE:", True, (200, 200, 200)), (620, 195))

    botoes = [
        (h_menu.btn_facil_rect, "FÁCIL", "Facil"),
        (h_menu.btn_medio_rect, "MÉDIO", "Medio"),
        (h_menu.btn_dificil_rect, "DIFÍCIL", "Dificil")
    ]

    for rect, label_txt, id_dif in botoes:
        cor = COR_BTN_SEL if h_menu.dificuldade_atual == id_dif else COR_BTN
        pygame.draw.rect(tela, cor, rect, border_radius=5)
        txt = fonte_s.render(label_txt, True, COR_TEXTO)
        tela.blit(txt, txt.get_rect(center=rect.center))

    # Volume
    tela.blit(label_fonte.render("VOLUME:", True, (200, 200, 200)), (620, 365))
    pygame.draw.line(tela, (100, 100, 100), (h_menu.slider_x_inicio, h_menu.slider_y), (h_menu.slider_x_fim, h_menu.slider_y), 3)
    knob_x = h_menu.obter_knob_pos()
    pygame.draw.circle(tela, (200, 200, 200), (knob_x, h_menu.slider_y), h_menu.knob_radius)
    pygame.draw.circle(tela, (255, 255, 255), (knob_x, h_menu.slider_y), h_menu.knob_radius - 2)


def criar_janela():
    pygame.init()
    
    largura, altura = 800, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Campo Minado - Pygame")

    caminho_sprites = os.path.join("imagens", "New Piskel.png")
    try:
        spritesheet = pygame.image.load(caminho_sprites).convert_alpha()
    except:
        spritesheet = pygame.Surface((32 * 20, 32))

    controller = TelaController(largura, altura)
    mapa = controller.inicializar_mapa(18, 18)
    
    # Inicia a música através do Handler de Áudio
    controller.handle_audio.iniciar_musica_fundo()

    tamanho_celula = 32
    largura_info = largura // 4
    offset_x = ((largura - largura_info) - (mapa.colunas * tamanho_celula)) // 2
    offset_y = (altura - (mapa.linhas * tamanho_celula)) // 2

    rodando = True
    while rodando:
        mapa = controller.handle_mapa._mapa
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            controller.tratar_evento(evento, offset_x=offset_x, offset_y=offset_y)

        tela.fill((30, 30, 30))
        desenhar_celulas(tela, spritesheet, mapa, controller, tamanho_celula, offset_x, offset_y)

        pygame.draw.rect(tela, (50, 50, 50), (largura - largura_info, 0, largura_info, altura))
        pygame.draw.line(tela, (100, 100, 100), (largura - largura_info, 0), (largura - largura_info, altura), 2)
        pygame.draw.line(tela, (100, 100, 100), (largura - largura_info, (altura // 10)), (largura, altura // 10), 2)

        desenhar_placar(tela, controller)
        desenhar_menu(tela, controller)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    criar_janela()
