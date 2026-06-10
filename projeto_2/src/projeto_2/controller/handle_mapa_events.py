import pygame
from projeto_2.model.mapa_quadrado import MapaQuadrado
from projeto_2.model.bandeira import Bandeira
from projeto_2.model.bomba import Bomba


class HandleMapa:
    def __init__(self, controller=None, mapa_quadrado=None):
        self._controller = controller
        self._mapa = mapa_quadrado
        self._primeiro_clique = True
        self._qtd_bombas = 40  # Valor padrão
        self._jogo_finalizado = False

    def inicializar_mapa(self, colunas: int, linhas: int) -> MapaQuadrado:
        """Cria e retorna um novo mapa."""
        self._mapa = MapaQuadrado(colunas, linhas)
        self._primeiro_clique = True
        self._jogo_finalizado = False
        # Notifica o placar para resetar o relógio
        if self._controller:
            self._controller.handle_placar.reiniciar()
        return self._mapa

    def set_qtd_bombas(self, qtd: int):
        """Define a quantidade de bombas para o próximo jogo."""
        self._qtd_bombas = qtd

    def obter_endereco_pela_posicao(
        self, pos_x: int, pos_y: int, offset_x: int = 0, offset_y: int = 0, tamanho_celula: int = 32
    ):
        """
        Converte coordenadas de pixels da tela para coordenadas (x, y) da grade,
        considerando os deslocamentos (offsets) de centralização.
        """
        if not self._mapa:
            return None

        grid_x = (pos_x - offset_x) // tamanho_celula
        grid_y = (pos_y - offset_y) // tamanho_celula

        if 0 <= grid_x < self._mapa.colunas and 0 <= grid_y < self._mapa.linhas:
            return (grid_x, grid_y)

        return None

    def obter_sprite_numero(self, valor: int) -> int:
        """
        Retorna a posição X do sprite para um determinado valor numérico.
        Segundo a regra: começa em 4*32 para o número 0.
        Assim: 0 -> 4*32, 1 -> 5*32, etc.
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

    def executar_acao_clique(self, x: int, y: int, botao: int):
        """
        Executa a ação correspondente ao botão do mouse.
        1: Botão Esquerdo -> Revelar célula.
        3: Botão Direito -> Adicionar/Alternar bandeira.
        """
        if not self._mapa or self._jogo_finalizado:
            return

        celula = self._mapa.obter_celula(x, y)
        if not celula:
            return

        if botao == 1:  # Esquerdo
            # Não permite revelar se a célula tiver uma bandeira
            if celula.obter_entidade(Bandeira):
                return

            if self._primeiro_clique:
                self._mapa.distribuir_bombas(x, y, self._qtd_bombas)
                self._primeiro_clique = False
                print("Bombas distribuídas.")
                # Inicia o relógio no primeiro clique
                if self._controller:
                    self._controller.handle_placar.iniciar()

            if self._mapa.revelar(x, y):
                # Game Over
                self._jogo_finalizado = True
                # Para o relógio
                if self._controller:
                    self._controller.handle_placar.parar()
                
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

    def processar_evento(self, evento, offset_x: int = 0, offset_y: int = 0):
        """Trata apenas eventos de clique do mouse (MOUSEBUTTONDOWN)."""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            grid_pos = self.obter_endereco_pela_posicao(
                evento.pos[0], evento.pos[1], offset_x, offset_y
            )
            if grid_pos:
                self.executar_acao_clique(grid_pos[0], grid_pos[1], evento.button)
