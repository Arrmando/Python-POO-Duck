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

    def _definir_id_persistencia(self, novo_id: int) -> None:
        """Método interno para a camada de persistência atribuir o ID incremental."""
        # getattr busca o '_id' dentro da classe filha (Ingrediente/HomemHora).
        # Se não achar nada ou for None, o padrão é None.
        id_atual = getattr(self, "_id", None)

        if id_atual is not None:
            raise ValueError(
                "O ID deste insumo já foi definido e não pode ser alterado."
            )

        # setattr injeta o valor direto na variável '_id' da classe filha
        setattr(self, "_id", novo_id)
