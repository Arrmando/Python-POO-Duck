from .entidade import Entidade


class Bomba(Entidade):
    def __init__(self, id: int, status: bool, sprite: int):
        super().__init__(id, status, sprite)
        self._sprite = 32 * 2
        self._status = False

    def explodir(self):
        self._status = True
        self._sprite = 32 * 3

    def identificar(self) -> str:
        return "Bomba"
