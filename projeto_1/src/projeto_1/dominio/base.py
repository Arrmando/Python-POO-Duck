from abc import ABC, abstractmethod


class PrecoComposto(ABC):
    @abstractmethod
    def calcular_total(self) -> float: ...


class Insumo(PrecoComposto):
    @property
    @abstractmethod
    def id(self): ...

    @property
    @abstractmethod
    def nome(self) -> str: ...

    @property
    @abstractmethod
    def unidade(self) -> str: ...

    @property
    @abstractmethod
    def quantidade(self) -> int: ...

    @property
    @abstractmethod
    def preco_base(self) -> float: ...

    @abstractmethod
    def __str__(self) -> str: ...
