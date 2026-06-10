from .handle_mapa_events import HandleMapa
from .handle_menu_events import HandleMenu
from .handle_placar_events import HandlePlacar


class TelaController:
    def __init__(self, mapa_quadrado=None):
        self.handle_mapa = HandleMapa(mapa_quadrado)
        self.handle_menu = HandleMenu()
        self.handle_placar = HandlePlacar()

    def inicializar_mapa(self, colunas: int, linhas: int):
        """Encaminha o pedido de inicialização para o handle_mapa."""
        return self.handle_mapa.inicializar_mapa(colunas, linhas)

    def tratar_evento(self, evento, offset_x: int = 0, offset_y: int = 0):
        """Distribui o evento para os handlers específicos, passando o offset do mapa."""
        self.handle_mapa.processar_evento(evento, offset_x, offset_y)
        self.handle_menu.processar_evento(evento)
        self.handle_placar.processar_evento(evento)
