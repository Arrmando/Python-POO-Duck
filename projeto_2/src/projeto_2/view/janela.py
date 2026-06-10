import pygame
import sys
import os
from projeto_2.controller.tela_controller import TelaController


def desenhar_celulas(tela, spritesheet, mapa, controller, tamanho_celula, offset_x, offset_y):
    """
    Função dedicada a exibir cada célula.
    A Visão não sabe mais o que são Bombas ou Bandeiras, ela apenas
    desenha os sprites que o Controlador indica.
    """
    for y in range(mapa.linhas):
        for x in range(mapa.colunas):
            celula = mapa.obter_celula(x, y)
            if not celula:
                continue

            pos_tela = (x * tamanho_celula + offset_x, y * tamanho_celula + offset_y)

            # 1. Desenha o sprite base da célula (definido no modelo)
            rect_base = pygame.Rect(celula.sprite, 0, tamanho_celula, tamanho_celula)
            tela.blit(spritesheet, pos_tela, rect_base)

            # 2. Desenha sprites sobrepostos indicados pelo Controlador
            sprites_extras = controller.handle_mapa.obter_sprites_sobrepostos(celula)
            for sprite_x in sprites_extras:
                rect_extra = pygame.Rect(sprite_x, 0, tamanho_celula, tamanho_celula)
                tela.blit(spritesheet, pos_tela, rect_extra)


def criar_janela():
    # Inicializa o Pygame
    pygame.init()

    # Configurações da janela
    largura = 800
    altura = 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Campo Minado - Pygame")

    # Carregamento de Recursos
    caminho_sprites = os.path.join("imagens", "New Piskel.png")
    try:
        spritesheet = pygame.image.load(caminho_sprites).convert_alpha()
    except pygame.error:
        print(f"Erro: Não foi possível carregar a imagem em {caminho_sprites}")
        spritesheet = pygame.Surface((32 * 20, 32))

    # Inicialização do Controller e Mapa
    controller = TelaController()
    mapa = controller.inicializar_mapa(18, 18)

    # Lógica de Centralização
    tamanho_celula = 32
    largura_info = largura // 4
    largura_disponivel = largura - largura_info
    altura_disponivel = altura
    
    offset_x = (largura_disponivel - (mapa.colunas * tamanho_celula)) // 2
    offset_y = (altura_disponivel - (mapa.linhas * tamanho_celula)) // 2

    # Cores
    COR_FUNDO = (30, 30, 30)

    # Loop principal
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            controller.tratar_evento(evento, offset_x=offset_x, offset_y=offset_y)

        tela.fill(COR_FUNDO)
        desenhar_celulas(tela, spritesheet, mapa, controller, tamanho_celula, offset_x, offset_y)

        # Painel lateral
        pygame.draw.rect(tela, (50, 50, 50), (largura - largura_info, 0, largura_info, altura))
        pygame.draw.line(tela, (100, 100, 100), (largura - largura_info, 0), (largura - largura_info, altura), 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    criar_janela()
