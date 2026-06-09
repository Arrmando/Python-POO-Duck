import pygame
import sys

def criar_janela():
    # Inicializa o Pygame
    pygame.init()

    # Configurações da janela
    largura = 800
    altura = 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Janela Básica Pygame")

    # Cores
    COR_FUNDO = (30, 30, 30)  # Cinza escuro
    COR_CIRCULO = (0, 255, 128) # Verde água

    # Loop principal
    rodando = True
    while rodando:
        # Gerenciamento de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Desenho
        tela.fill(COR_FUNDO)
        
        # Desenha um círculo no centro apenas para ter algo visual
        pygame.draw.circle(tela, COR_CIRCULO, (largura // 2, altura // 2), 50)
        pygame.draw.rect(tela, (255, 0, 0), ((largura - (largura// 4)) , 0 , (largura // 4), altura)) # Desenha um retângulo vermelho no lado direito da tela Para representar a área de informações 
        pygame.draw.rect(tela, (0, 0, 255), ((largura - (largura// 4)), 0, (largura - (largura// 4)), (altura// 6))) # Desenha um retângulo ciano no canto superior esquerdo da tela para representar a
      
        # Atualiza a tela
        pygame.display.flip()
    # Encerra o Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    criar_janela()