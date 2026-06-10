from .handle_mapa_events import HandleMapa
from .handle_menu_events import HandleMenu
from .handle_placar_events import HandlePlacar
from .handle_audio_events import HandleAudio


class TelaController:
    def __init__(self, largura: int = 800, altura: int = 600, mapa_quadrado=None):
        self.largura = largura
        self.altura = altura
        self.largura_info = largura // 4
        
        # Definição das áreas
        self.area_mapa = (0, 0, largura - self.largura_info, altura)
        self.area_placar = (largura - self.largura_info, 0, self.largura_info, altura // 10)
        self.area_menu = (
            largura - self.largura_info, 
            altura // 10, 
            self.largura_info, 
            altura - (altura // 10)
        )

        # Instanciação dos handlers
        self.handle_audio = HandleAudio()
        self.handle_mapa = HandleMapa(controller=self, mapa_quadrado=mapa_quadrado)
        self.handle_menu = HandleMenu(controller=self)
        self.handle_placar = HandlePlacar()

    def inicializar_mapa(self, colunas: int, linhas: int):
        return self.handle_mapa.inicializar_mapa(colunas, linhas)

    def _esta_dentro(self, pos, area):
        px, py = pos
        ax, ay, aw, ah = area
        return ax <= px < ax + aw and ay <= py < ay + ah

    def tratar_evento(self, evento, offset_x: int = 0, offset_y: int = 0):
        # O Handler de áudio pode escutar eventos globais (teclado, etc)
        self.handle_audio.processar_evento(evento)
        
        if hasattr(evento, "pos"):
            pos = evento.pos
            if self._esta_dentro(pos, self.area_mapa):
                self.handle_mapa.processar_evento(evento, offset_x, offset_y)
            elif self._esta_dentro(pos, self.area_placar):
                self.handle_placar.processar_evento(evento)
            elif self._esta_dentro(pos, self.area_menu):
                self.handle_menu.processar_evento(evento)
