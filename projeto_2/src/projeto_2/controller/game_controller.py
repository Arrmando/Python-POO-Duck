import sys

import pygame

from .handle_audio_events import HandleAudio
from .handle_mapa_events import HandleMapa
from .handle_menu_events import HandleMenu
from .handle_placar_events import HandlePlacar


class GameController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.largura = view.largura
        self.altura = view.altura
        self.largura_info = self.largura // 4

        # Definição das áreas (Lógica de layout de alto nível)
        self.area_mapa = (0, 0, self.largura - self.largura_info, self.altura)
        self.area_placar = (
            self.largura - self.largura_info,
            0,
            self.largura_info,
            self.altura // 10,
        )
        self.area_menu = (
            self.largura - self.largura_info,
            self.altura // 10,
            self.largura_info,
            self.altura - (self.altura // 10),
        )

        # Instanciação dos handlers
        self.handle_audio = HandleAudio()
        self.handle_mapa = HandleMapa(
            model.game_state, controller=self, mapa_quadrado=model.mapa
        )
        self.handle_menu = HandleMenu(model.game_state, controller=self)
        self.handle_placar = HandlePlacar(model.game_state)

    def inicializar_mapa(self, colunas: int, linhas: int):
        mapa = self.handle_mapa.inicializar_mapa(colunas, linhas)
        self.model.mapa = mapa
        self.view.mapa_view.mapa_ro = mapa
        self.view.calcular_offsets()
        return mapa

    def _esta_dentro(self, pos, area):
        px, py = pos
        ax, ay, aw, ah = area
        return ax <= px < ax + aw and ay <= py < ay + ah

    def tratar_evento(self, evento):
        # O Handler de áudio pode escutar eventos globais (teclado, etc)
        self.handle_audio.processar_evento(evento)

        if hasattr(evento, "pos"):
            pos = evento.pos
            if self._esta_dentro(pos, self.area_mapa):
                grid_pos = self.view.converter_tela_para_grade(pos)
                self.handle_mapa.processar_evento(evento, grid_pos=grid_pos)
            elif self._esta_dentro(pos, self.area_placar):
                self.handle_placar.processar_evento(evento)
            elif self._esta_dentro(pos, self.area_menu):
                view_geometry = self.view.obter_geometria()
                self.handle_menu.processar_evento(evento, view_geometry=view_geometry)

    def _obter_estado_atual(self):
        """Captura um snapshot do estado atual para a View."""
        return {
            "area_placar": self.area_placar,
        }

    def run(self):
        """Orquestra o loop principal do jogo."""
        self.handle_audio.iniciar_musica_fundo()

        # O mapa inicial já foi passado no construtor e está no handle_mapa
        self.view.calcular_offsets()

        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                self.tratar_evento(evento)
            estado = self._obter_estado_atual()
            self.view.render(estado)

        pygame.quit()
        sys.exit()
