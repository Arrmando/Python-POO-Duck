from projeto_1.dominio.base import Item
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
