import pygame


class HandleMenu:
    def __init__(self, controller=None):
        self._controller = controller
        
        # O menu começa em X=600 (para largura 800)
        # 1. Botão REINICIAR
        self.btn_reiniciar_rect = pygame.Rect(620, 80, 160, 40)
        
        # 2. Botão PLACAR
        self.btn_placar_rect = pygame.Rect(620, 140, 160, 40)
        
        # 3. Botões de Dificuldade
        self.btn_facil_rect = pygame.Rect(620, 220, 160, 35)
        self.btn_medio_rect = pygame.Rect(620, 265, 160, 35)
        self.btn_dificil_rect = pygame.Rect(620, 310, 160, 35)
        
        # 4. Controle de Volume (Slider)
        self.slider_x_inicio = 630
        self.slider_x_fim = 770
        self.slider_y = 400
        self.volume = 0.5  # Valor entre 0.0 e 1.0
        self.knob_radius = 8
        self._arrastando_volume = False
        
        self.dificuldade_atual = "Medio" # Padrão

    def obter_knob_pos(self):
        """Calcula a posição X do círculo baseada no volume atual."""
        largura_total = self.slider_x_fim - self.slider_x_inicio
        return int(self.slider_x_inicio + (self.volume * largura_total))

    def processar_evento(self, evento):
        """Trata cliques e arraste no menu."""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos
            # Botões normais
            if self.btn_reiniciar_rect.collidepoint(pos):
                self.reiniciar_jogo()
            elif self.btn_placar_rect.collidepoint(pos):
                self.abrir_placar()
            elif self.btn_facil_rect.collidepoint(pos):
                self.mudar_dificuldade("Facil", 10)
            elif self.btn_medio_rect.collidepoint(pos):
                self.mudar_dificuldade("Medio", 40)
            elif self.btn_dificil_rect.collidepoint(pos):
                self.mudar_dificuldade("Dificil", 99)
            
            # Verifica clique no knob do volume
            knob_x = self.obter_knob_pos()
            distancia = ((pos[0] - knob_x)**2 + (pos[1] - self.slider_y)**2)**0.5
            if distancia <= self.knob_radius + 5: # Margem extra para facilitar clique
                self._arrastando_volume = True

        elif evento.type == pygame.MOUSEBUTTONUP:
            self._arrastando_volume = False

        elif evento.type == pygame.MOUSEMOTION:
            if self._arrastando_volume:
                pos_x = evento.pos[0]
                # Limita o movimento à reta
                pos_x = max(self.slider_x_inicio, min(pos_x, self.slider_x_fim))
                
                # Atualiza o valor do volume
                largura_total = self.slider_x_fim - self.slider_x_inicio
                self.volume = (pos_x - self.slider_x_inicio) / largura_total
                
                # Sincroniza o volume com o Handler de Áudio
                if self._controller:
                    self._controller.handle_audio.ajustar_volume(self.volume)

    def reiniciar_jogo(self):
        """Pede ao controlador principal para reiniciar o mapa."""
        if self._controller:
            print("Reiniciando jogo...")
            self._controller.inicializar_mapa(18, 18)

    def abrir_placar(self):
        """Lógica para abrir a visualização do placar."""
        print("Abrindo Placar...")

    def mudar_dificuldade(self, nome: str, bombas: int):
        """Altera a dificuldade e reinicia o jogo imediatamente."""
        self.dificuldade_atual = nome
        if self._controller:
            print(f"Mudando dificuldade para: {nome} ({bombas} bombas)")
            self._controller.handle_mapa.set_qtd_bombas(bombas)
            self.reiniciar_jogo()
