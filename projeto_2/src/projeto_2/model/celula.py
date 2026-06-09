from .bomba import Bomba
from .bandeira import Bandeira
from .entidade import Entidade
from typing import List, Type, TypeVar

T = TypeVar("T", bound=Entidade)


class Celula:
    def __init__(self, address: int, status: bool = True, valor: int = 0, sprite: int = 0):
        """
        status: True para escondida (padrão), False para cavada.
        """
        self._address = address
        self._status = status
        self._valor = valor
        self._sprite = sprite
        self._entidades: List[Entidade] = []

    @property
    def address(self):
        return self._address

    @property
    def status(self):
        return self._status

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo_valor: int):
        self._valor = novo_valor

    @property
    def sprite(self):
        return self._sprite

    @property
    def entidades(self) -> List[Entidade]:
        return self._entidades

    def cavar(self):
        """
        Muda o status para False (cavada), mas apenas se a célula estiver escondida (True).
        """
        if self._status:
            self._status = False
            self._sprite = 32 * 1

    def _tem_entidade_do_tipo(self, tipo: Type[Entidade]) -> bool:
        return any(isinstance(e, tipo) for e in self._entidades)

    def adicionar_bandeira(self, bandeira: Bandeira):
        if self._tem_entidade_do_tipo(Bandeira):
            raise ValueError("Esta célula já possui uma bandeira.")
        self._entidades.append(bandeira)

    def adicionar_bomba(self, bomba: Bomba):
        if self._tem_entidade_do_tipo(Bomba):
            raise ValueError("Esta célula já possui uma bomba.")
        self._entidades.append(bomba)

    def remover_entidade(self, tipo: Type[Entidade]):
        self._entidades = [e for e in self._entidades if not isinstance(e, tipo)]

    def obter_entidade(self, tipo: Type[T]) -> T | None:
        for e in self._entidades:
            if isinstance(e, tipo):
                return e
        return None
