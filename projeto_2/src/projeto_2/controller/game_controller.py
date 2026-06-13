import sys

import pygame

from projeto_2.constants import (
    CELULA_CLICK,
    DIFICULDADE_ALTERADA,
    PLACAR_CLICK,
    REINICIAR_CLICK,
    VOLUME_ALTERADO,
)

from .handle_audio_events import HandleAudio
from .handle_mapa_events import HandleMapa


class GameController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.largura = view.largura
        self.altura = view.altura
        self.largura_info = self.largura // 4

        # Definição das áreas (Lógica de layout de alto nível)
        self.area_placar = (
            self.largura - self.largura_info,
            0,
            self.largura_info,
            self.altura // 10,
        )

        # Instanciação dos handlers
        self.handle_audio = HandleAudio(model.game_state)
        self.handle_mapa = HandleMapa(model.game_state, mapa_quadrado=model.mapa)

    def inicializar_mapa(self, colunas: int, linhas: int):
        mapa = self.handle_mapa.inicializar_mapa(colunas, linhas)
        self.model.mapa = mapa
        self.view.mapa_view.mapa_ro = mapa
        self.view.calcular_offsets()
        return mapa

    def tratar_evento_bruto(self, evento):
        """Passa eventos brutos para a View traduzir, e para handlers globais."""
        self.handle_audio.processar_evento(evento)
        self.view.handle_event(evento)

    def processar_evento_jogo(self, evento):
        """Reage aos eventos customizados emitidos pelas Views."""
        if evento.type == CELULA_CLICK:
            gx, gy = evento.pos
            self.handle_mapa.executar_acao_clique(gx, gy, evento.button)

        elif evento.type == REINICIAR_CLICK:
            print("Reiniciando jogo...")
            self.inicializar_mapa(18, 18)

        elif evento.type == PLACAR_CLICK:
            print("Abrindo Placar...")

        elif evento.type == DIFICULDADE_ALTERADA:
            nome = evento.nome
            bombas = evento.bombas
            print(f"Mudando dificuldade para: {nome} ({bombas} bombas)")
            self.model.game_state.qtd_bombas = bombas
            self.model.game_state.dificuldade = nome
            self.inicializar_mapa(18, 18)

        elif evento.type == VOLUME_ALTERADO:
            self.model.game_state.volume = evento.volume
            self.handle_audio.ajustar_volume(evento.volume)

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
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    rodando = False

                self.tratar_evento_bruto(evento)
                self.processar_evento_jogo(evento)

            estado = self._obter_estado_atual()
            self.view.render(estado)

        pygame.quit()
        sys.exit()
