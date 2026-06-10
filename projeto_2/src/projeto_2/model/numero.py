from .entidade import Entidade


class Numero(Entidade):
    def __init__(self, valor: int, sprite: int):
        # Usamos o valor como ID para simplificar
        super().__init__(id=valor, status=False, sprite=sprite)
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def identificar(self) -> str:
        return f"Numero_{self._valor}"
