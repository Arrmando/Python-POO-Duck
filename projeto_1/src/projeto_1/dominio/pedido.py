from datetime import datetime

from projeto_1.dominio.base import Item, PrecoComposto
from projeto_1.dominio.receita import Receita


class ItemPedido(Item):
    """Representa um item específico dentro de um pedido.

    Associa uma receita a um coeficiente (quantidade solicitada).
    """

    def __init__(self, receita: Receita, coeficiente: float) -> None:

        if receita is None:
            raise ValueError(
                "O item da receita precisa estar vinculado a uma receita válida ."
            )
        if coeficiente <= 0:
            raise ValueError("O coeficiente do item deve ser maior que zero.")

        self._receita = receita
        self._coeficiente = coeficiente

    @property
    def receita(self) -> Receita:
        return self._receita

    @property
    def coeficiente(self) -> float:
        return self._coeficiente

    def calcular_total(self) -> float:
        """Calcula o preço do item (preço da receita * coeficiente)."""
        return self._receita.calcular_total() * self._coeficiente


class Pedido(PrecoComposto):
    """Representa um pedido no sistema.

    Um pedido é composto por vários ItemPedido e calcula seu valor total
    somando o valor de cada item.
    """

    def __init__(
        self,
        cliente: str,
        id: int | None = None,
    ) -> None:
        if not cliente or not cliente.strip():
            raise ValueError("O nome do cliente não pode ser vazio.")

        self._id = id
        self._cliente = cliente.strip()
        self._data_pedido = datetime.now()
        self._itens: list[ItemPedido] = []

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def cliente(self) -> str:
        return self._cliente

    @property
    def data_pedido(self) -> datetime:
        return self._data_pedido

    @property
    def itens(self) -> list[ItemPedido]:
        return list(self._itens)

    def adicionar_item(self, item: ItemPedido) -> None:
        """Adiciona um novo item ao pedido."""
        if not isinstance(item, ItemPedido):
            raise ValueError("Apenas objetos do tipo ItemPedido podem ser adicionados.")
        self._itens.append(item)

    def remover_item(self, item: ItemPedido) -> None:
        """Remove um item do pedido."""
        if item not in self._itens:
            raise ValueError("O item informado não pertence a este pedido.")
        self._itens.remove(item)

    def calcular_total(self) -> float:
        """Calcula o preço total do pedido somando o valor de cada item."""
        return sum(item.calcular_total() for item in self._itens)
