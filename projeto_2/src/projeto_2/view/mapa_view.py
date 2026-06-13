import pygame

from projeto_2.constants import CELULA_CLICK
from projeto_2.model.bandeira import Bandeira
from projeto_2.model.bomba import Bomba
from projeto_2.utils import post_evento


class MapaView:
    def __init__(self, mapa_ro, tamanho_celula: int = 32):
        self.mapa_ro = mapa_ro
        self.tamanho_celula = tamanho_celula
        self.offset_x = 0
        self.offset_y = 0

    def calcular_offsets(self, largura_area: int, altura_area: int):
        """Calcula a centralização do mapa baseado na grade e na área disponível."""
        self.offset_x = (
            largura_area - (self.mapa_ro.colunas * self.tamanho_celula)
        ) // 2
        self.offset_y = (altura_area - (self.mapa_ro.linhas * self.tamanho_celula)) // 2
        return self.offset_x, self.offset_y

    def converter_tela_para_grade(self, pos):
        """Converte coordenadas da tela para (x, y) da grade."""
        px, py = pos
        gx = (px - self.offset_x) // self.tamanho_celula
        gy = (py - self.offset_y) // self.tamanho_celula
        return int(gx), int(gy)

    def obter_sprite_numero(self, valor: int) -> int:
        """
        Retorna a posição X do sprite para um determinado valor numérico.
        Segundo a regra: começa em 4*32 para o número 0.
        """
        return (4 + valor) * 32

    def obter_sprites_sobrepostos(self, celula) -> list[int]:
        """
        Analisa a célula e retorna uma lista de posições X dos sprites
        que devem ser desenhados sobre a base.
        """
        sprites = []

        if celula.status:  # Célula escondida
            bandeira = celula.obter_entidade(Bandeira)
            if bandeira:
                sprites.append(bandeira.sprite)
        else:  # Célula revelada
            # 1. Adiciona número se houver
            if celula.valor > 0:
                sprites.append(self.obter_sprite_numero(celula.valor))

            # 2. Adiciona bomba se houver
            bomba = celula.obter_entidade(Bomba)
            if bomba:
                sprites.append(bomba.sprite)

        return sprites

    def handle_event(self, event):
        """
        Traduz eventos brutos do pygame em eventos de jogo (CELULA_CLICK).
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid_pos = self.converter_tela_para_grade(event.pos)
            gx, gy = grid_pos
            if 0 <= gx < self.mapa_ro.colunas and 0 <= gy < self.mapa_ro.linhas:
                post_evento(CELULA_CLICK, pos=grid_pos, button=event.button)

    def desenhar(self, tela, spritesheet):
        """Exibe cada célula e seus sprites sobrepostos (números, bombas, bandeiras)."""
        for y in range(self.mapa_ro.linhas):
            for x in range(self.mapa_ro.colunas):
                celula = self.mapa_ro.obter_celula(x, y)
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
                sprites_extras = self.obter_sprites_sobrepostos(celula)
                for sprite_x in sprites_extras:
                    rect_extra = pygame.Rect(
                        sprite_x, 0, self.tamanho_celula, self.tamanho_celula
                    )
                    tela.blit(spritesheet, pos_tela, rect_extra)
