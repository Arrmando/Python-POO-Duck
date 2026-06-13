import pygame

from projeto_2.model.bandeira import Bandeira
from projeto_2.model.bomba import Bomba
from projeto_2.model.mapa_quadrado import MapaQuadrado


class HandleMapa:
    def __init__(self, game_state, controller=None, mapa_quadrado=None):
        self._controller = controller
        self._mapa = mapa_quadrado
        self._game_state = game_state

    def inicializar_mapa(self, colunas: int, linhas: int) -> MapaQuadrado:
        """Cria e retorna um novo mapa."""
        self._mapa = MapaQuadrado(colunas, linhas)
        self._game_state.primeiro_clique = True
        self._game_state.jogo_finalizado = False
        self._game_state.reiniciar_timer()
        return self._mapa

    def set_qtd_bombas(self, qtd: int):
        """Define a quantidade de bombas para o próximo jogo."""
        self._game_state.qtd_bombas = qtd

    def executar_acao_clique(self, x: int, y: int, botao: int):
        """
        Executa a ação correspondente ao botão do mouse.
        1: Botão Esquerdo -> Revelar célula.
        3: Botão Direito -> Adicionar/Alternar bandeira.
        """
        if not self._mapa or self._game_state.jogo_finalizado:
            return

        celula = self._mapa.obter_celula(x, y)
        if not celula:
            return

        if botao == 1:  # Esquerdo
            # Não permite revelar se a célula tiver uma bandeira
            if celula.obter_entidade(Bandeira):
                return

            if self._game_state.primeiro_clique:
                self._mapa.distribuir_bombas(x, y, self._game_state.qtd_bombas)
                self._game_state.primeiro_clique = False
                print("Bombas distribuídas.")
                # Inicia o relógio no primeiro clique
                self._game_state.iniciar_timer()

            if self._mapa.revelar(x, y):
                # Game Over
                self._game_state.jogo_finalizado = True
                self._game_state.parar_timer()

                # Executa explodir apenas na bomba que foi clicada
                bomba_clicada = celula.obter_entidade(Bomba)
                if bomba_clicada:
                    bomba_clicada.explodir()

                # Revela todas as células do mapa (sem recursão redundante)
                print("GAME OVER! Revelando tabuleiro...")
                for ry in range(self._mapa.linhas):
                    for rx in range(self._mapa.colunas):
                        c = self._mapa.obter_celula(rx, ry)
                        if c:
                            c.cavar()

        elif botao == 3:  # Direito
            if celula.status:
                if celula.obter_entidade(Bandeira):
                    celula.remover_entidade(Bandeira)
                else:
                    nova_bandeira = Bandeira(id=celula.address, status=True, sprite=0)
                    celula.adicionar_bandeira(nova_bandeira)

    def processar_evento(self, evento, grid_pos=None):
        """Trata apenas eventos de clique do mouse (MOUSEBUTTONDOWN)."""
        if evento.type == pygame.MOUSEBUTTONDOWN and grid_pos:
            self.executar_acao_clique(grid_pos[0], grid_pos[1], evento.button)
