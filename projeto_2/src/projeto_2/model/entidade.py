from abc import ABC, abstractmethod


class Entidade(ABC):
    def __init__(self, id: int, status: bool, sprite: int):
        self._id = id
        self._status = status
        self._sprite = sprite

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @property
    def sprite(self):
        return self._sprite

    @abstractmethod
    def identificar(self) -> str:
        """Retorna uma string identificando o tipo de entidade."""
        pass
