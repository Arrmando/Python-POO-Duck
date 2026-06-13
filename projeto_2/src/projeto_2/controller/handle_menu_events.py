import pygame


class HandleMenu:
    def __init__(self, game_state):
        self._game_state = game_state
        self._arrastando_volume = False

    @property
    def volume(self):
        return self._game_state.volume

    @volume.setter
    def volume(self, valor):
        self._game_state.volume = valor

    @property
    def dificuldade_atual(self):
        return self._game_state.dificuldade

    @dificuldade_atual.setter
    def dificuldade_atual(self, valor):
        self._game_state.dificuldade = valor

    def obter_knob_pos(self, slider_x_inicio=630, slider_x_fim=770):
        """Calcula a posição X do círculo baseada no volume atual."""
        largura_total = slider_x_fim - slider_x_inicio
        return int(slider_x_inicio + (self.volume * largura_total))

    def processar_evento(self, evento, view_geometry=None):
        """
        Trata cliques e arraste no menu.
        Retorna um dicionário com ações solicitadas (ex: {'acao': 'reiniciar'}).
        """
        if not view_geometry:
            return None

        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos
            # Botões normais
            if view_geometry["btn_reiniciar"].collidepoint(pos):
                return {"acao": "reiniciar"}
            elif view_geometry["btn_placar"].collidepoint(pos):
                return {"acao": "abrir_placar"}
            elif view_geometry["btn_facil"].collidepoint(pos):
                return {"acao": "mudar_dificuldade", "nome": "Facil", "bombas": 10}
            elif view_geometry["btn_medio"].collidepoint(pos):
                return {"acao": "mudar_dificuldade", "nome": "Medio", "bombas": 40}
            elif view_geometry["btn_dificil"].collidepoint(pos):
                return {"acao": "mudar_dificuldade", "nome": "Dificil", "bombas": 99}

            # Verifica clique no knob do volume
            slider = view_geometry["slider"]
            knob_x = self.obter_knob_pos(slider["x_inicio"], slider["x_fim"])
            distancia = ((pos[0] - knob_x) ** 2 + (pos[1] - slider["y"]) ** 2) ** 0.5
            if (
                distancia <= slider["knob_radius"] + 5
            ):  # Margem extra para facilitar clique
                self._arrastando_volume = True

        elif evento.type == pygame.MOUSEBUTTONUP:
            self._arrastando_volume = False

        elif evento.type == pygame.MOUSEMOTION:
            if self._arrastando_volume:
                slider = view_geometry["slider"]
                pos_x = evento.pos[0]
                # Limita o movimento à reta
                pos_x = max(slider["x_inicio"], min(pos_x, slider["x_fim"]))

                # Atualiza o valor do volume
                largura_total = slider["x_fim"] - slider["x_inicio"]
                self.volume = (pos_x - slider["x_inicio"]) / largura_total
                
                return {"acao": "ajustar_volume", "volume": self.volume}

        return None
