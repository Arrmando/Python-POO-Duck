import pygame

from projeto_2.constants import CELULA_CLICK
from projeto_2.model.bandeira import Bandeira
from projeto_2.model.bomba import Bomba
from projeto_2.utils import post_evento

from .base_view import BaseView
from .colors import Colors
from .widget_views import Text


class MapaView(BaseView):
    def __init__(
        self,
        *,
        mapa_ro,
        spritesheet,
        area: tuple[int, int],
        tamanho_celula: int = 32,
    ):
        self.mapa_ro = mapa_ro
        self.spritesheet = spritesheet
        self.area = area
        self.tamanho_celula = tamanho_celula
        # Offset relativo ao pai (calculado dinamicamente)
        self.local_offset = (0, 0)

        # Widget de texto reutilizável para os números
        self._text_widget = Text(
            pos=(0, 0),
            texto="",
            cor=Colors.TEXT_DEFAULT,
            tamanho=22,
            bold=True,
            fonte_nome="Arial",
        )

    def _atualizar_offsets(self):
        """Calcula a centralização do mapa baseada na área disponível."""
        offset_x = (self.area[0] - (self.mapa_ro.colunas * self.tamanho_celula)) // 2
        offset_y = (self.area[1] - (self.mapa_ro.linhas * self.tamanho_celula)) // 2
        self.local_offset = (offset_x, offset_y)

    def _obter_cor_numero(self, valor: int):
        cores = {
            1: Colors.NUM_1,
            2: Colors.NUM_2,
            3: Colors.NUM_3,
            4: Colors.NUM_4,
            5: Colors.NUM_5,
            6: Colors.NUM_6,
            7: Colors.NUM_7,
            8: Colors.NUM_8,
        }
        return cores.get(valor, Colors.TEXT_DEFAULT)

    def converter_tela_para_grade(self, pos, parent_offset=(0, 0)):
        """Converte coordenadas da tela para (x, y) da grade, considerando offsets."""
        self._atualizar_offsets()
        ox, oy = parent_offset
        px, py = pos
        gx = (px - (ox + self.local_offset[0])) // self.tamanho_celula
        gy = (py - (oy + self.local_offset[1])) // self.tamanho_celula
        return int(gx), int(gy)

    def obter_sprites_sobrepostos(self, celula) -> list[int]:
        """Retorna sprites que NÃO são números (bombas e bandeiras)."""
        sprites = []
        if celula.status:  # Escondida
            bandeira = celula.obter_entidade(Bandeira)
            if bandeira:
                sprites.append(bandeira.sprite)
        else:  # Revelada
            bomba = celula.obter_entidade(Bomba)
            if bomba:
                sprites.append(bomba.sprite)
        return sprites

    def handle_event(self, event, offset: tuple[float, float] = (0, 0)):
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid_pos = self.converter_tela_para_grade(event.pos, offset)
            gx, gy = grid_pos
            if 0 <= gx < self.mapa_ro.colunas and 0 <= gy < self.mapa_ro.linhas:
                post_evento(CELULA_CLICK, pos=grid_pos, button=event.button)

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        self._atualizar_offsets()
        ox, oy = offset
        ax = ox + self.local_offset[0]
        ay = oy + self.local_offset[1]

        for y in range(self.mapa_ro.linhas):
            for x in range(self.mapa_ro.colunas):
                celula = self.mapa_ro.obter_celula(x, y)
                if not celula:
                    continue

                pos_tela = (
                    x * self.tamanho_celula + ax,
                    y * self.tamanho_celula + ay,
                )

                # 1. Sprite base da célula (fundo escondido ou revelado)
                rect_base = pygame.Rect(
                    celula.sprite, 0, self.tamanho_celula, self.tamanho_celula
                )
                tela.blit(self.spritesheet, pos_tela, rect_base)

                # 2. Se revelada e tiver valor, desenha o número com a cor correta
                if not celula.status and celula.valor > 0:
                    self._text_widget.texto = str(celula.valor)
                    self._text_widget.cor = self._obter_cor_numero(celula.valor)
                    # Centraliza o texto na célula
                    rect_celula = pygame.Rect(
                        pos_tela[0],
                        pos_tela[1],
                        self.tamanho_celula,
                        self.tamanho_celula,
                    )
                    self._text_widget.centralizar_em_rect = rect_celula
                    # Desenha sem offset extra pois pos_tela já é absoluto
                    self._text_widget.desenhar(tela, offset=(0, 0))

                # 3. Desenha outras entidades sobrepostas (bombas, bandeiras)
                sprites_extras = self.obter_sprites_sobrepostos(celula)
                for sprite_x in sprites_extras:
                    rect_extra = pygame.Rect(
                        sprite_x, 0, self.tamanho_celula, self.tamanho_celula
                    )
                    tela.blit(self.spritesheet, pos_tela, rect_extra)
