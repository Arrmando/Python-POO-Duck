import pygame


class MapaView:
    def __init__(self, tamanho_celula: int = 32):
        self.tamanho_celula = tamanho_celula
        self.offset_x = 0
        self.offset_y = 0

    def calcular_offsets(
        self, largura_area: int, altura_area: int, colunas: int, linhas: int
    ):
        """Calcula a centralização do mapa baseado na grade e na área disponível."""
        self.offset_x = (largura_area - (colunas * self.tamanho_celula)) // 2
        self.offset_y = (altura_area - (linhas * self.tamanho_celula)) // 2
        return self.offset_x, self.offset_y

    def converter_tela_para_grade(self, pos):
        """Converte coordenadas da tela para (x, y) da grade."""
        px, py = pos
        gx = (px - self.offset_x) // self.tamanho_celula
        gy = (py - self.offset_y) // self.tamanho_celula
        return int(gx), int(gy)

    def desenhar(self, tela, spritesheet, mapa, mapa_handler):
        """Exibe cada célula e seus sprites sobrepostos (números, bombas, bandeiras)."""
        for y in range(mapa.linhas):
            for x in range(mapa.colunas):
                celula = mapa.obter_celula(x, y)
                if not celula:
                    continue

                pos_tela = (
                    x * self.tamanho_celula + self.offset_x,
                    y * self.tamanho_celula + self.offset_y,
                )

                # Sprite base da célula
                rect_base = pygame.Rect(
                    celula.sprite, 0, self.tamanho_celula, self.tamanho_celula
                )
                tela.blit(spritesheet, pos_tela, rect_base)

                # Sprites sobrepostos (números, bombas, bandeiras)
                sprites_extras = mapa_handler.obter_sprites_sobrepostos(celula)
                for sprite_x in sprites_extras:
                    rect_extra = pygame.Rect(
                        sprite_x, 0, self.tamanho_celula, self.tamanho_celula
                    )
                    tela.blit(spritesheet, pos_tela, rect_extra)
