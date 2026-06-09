from .entidade import Entidade


class Bandeira(Entidade):
    def __init__(self, id: int, status: bool, sprite: int):
        super().__init__(id, status, sprite)
        self._sprite = 32 * 14
        self._status = True

    def identificar(self) -> str:
        return "Bandeira"
