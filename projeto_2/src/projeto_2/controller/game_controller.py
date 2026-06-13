import sys

import pygame

from projeto_2.constants import (
    CELULA_CLICK,
    DIFICULDADE_ALTERADA,
    PLACAR_CLICK,
    REINICIAR_CLICK,
    VOLUME_ALTERADO,
)

from .audio_controller import AudioController
from .mapa_controller import MapaController


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

        # Instanciação dos handlers (agora Controllers)
        self.audio_controller = AudioController(model.game_state)
        self.mapa_controller = MapaController(
            model.game_state, mapa_quadrado=model.mapa
        )

    def inicializar_jogo(self, colunas: int, linhas: int):
        self.model.iniciar_jogo(colunas, linhas)
        self.view.calcular_offsets()

    def processar_evento_bruto(self, evento):
        """Recebe eventos do pygame (brutos) e repassa para que as views processem."""
        self.view.handle_event(evento)

    def processar_evento_jogo(self, evento):
        """Recebe eventos de jogo e delega sub-controllers para atuar nos models."""
        if evento.type == CELULA_CLICK:
            gx, gy = evento.pos
            if evento.button == 1:  # Esquerdo
                self.mapa_controller.handle_clique_esquerdo(gx, gy)
            elif evento.button == 3:  # Direito
                self.mapa_controller.handle_clique_direito(gx, gy)

        elif evento.type == REINICIAR_CLICK:
            print("Reiniciando jogo...")
            self.inicializar_jogo(18, 18)

        elif evento.type == PLACAR_CLICK:
            print("Abrindo Placar...")

        elif evento.type == DIFICULDADE_ALTERADA:
            nome = evento.nome
            bombas = evento.bombas
            print(f"Mudando dificuldade para: {nome} ({bombas} bombas)")
            self.model.game_state.qtd_bombas = bombas
            self.model.game_state.dificuldade = nome
            self.inicializar_jogo(18, 18)

        elif evento.type == VOLUME_ALTERADO:
            self.model.game_state.volume = evento.volume
            self.audio_controller.ajustar_volume(evento.volume)

    def _obter_estado_atual(self):
        """Captura um snapshot do estado atual para a View."""
        return {
            "area_placar": self.area_placar,
        }

    def run(self):
        """Orquestra o loop principal do jogo."""
        self.audio_controller.iniciar_musica_fundo()

        # O mapa inicial já foi passado no construtor
        self.view.calcular_offsets()

        rodando = True
        while rodando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    rodando = False

                self.processar_evento_bruto(evento)
                self.processar_evento_jogo(evento)

            estado = self._obter_estado_atual()
            self.view.render(estado)

        pygame.quit()
        sys.exit()
