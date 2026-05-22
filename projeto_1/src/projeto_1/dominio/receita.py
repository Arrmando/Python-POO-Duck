from src.projeto_1.dominio.base import Insumo, Item


class ItemReceita(Item):
    """Representa um item específico dentro de uma receita, associando um insumo

    a um coeficiente (quantidade utilizada).
    """

    def __init__(self, insumo: Insumo, coeficiente: float) -> None:
        if insumo is None:
            raise ValueError(
                "O item da receita precisa estar vinculado a um insumo válido."
            )
        if coeficiente <= 0:
            raise ValueError("O coeficiente do item deve ser maior que zero.")

        self._insumo = insumo
        self._coeficiente = coeficiente

    @property
    def insumo(self) -> Insumo:
        return self._insumo

    @property
    def coeficiente(self) -> float:
        """Implementa a propriedade obrigatória da classe abstrata Item."""
        return self._coeficiente

    def calcular_total(self) -> float:
        """Implementa o método obrigatório de PrecoComposto.

        Calcula o custo do item multiplicando o preço base do insumo pelo
        coeficiente usado.
        """
        return self._insumo.preco_base * self._coeficiente


class Receita:
    """Representa uma receita do sistema, agregando múltiplos itens."""

    def __init__(self, nome: str, instrucoes: str, id: int | None = None) -> None:
        if not nome or not nome.strip():
            raise ValueError("O nome da receita não pode ser vazio.")

        self._id = id
        self._nome = nome.strip()
        self._instrucoes = instrucoes
        self._itens: list[ItemReceita] = []

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def instrucoes(self) -> str:
        return self._instrucoes

    @property
    def itens(self) -> list[ItemReceita]:
        # Retorna uma cópia da lista para proteger contra mutações externas diretas
        return list(self._itens)

    def adicionar_item(self, item: ItemReceita) -> None:
        """Adiciona um novo item à receita."""
        if not isinstance(item, ItemReceita):
            raise ValueError(
                "Apenas objetos do tipo ItemReceita podem ser adicionados."
            )
        self._itens.append(item)

    def remover_item(self, item: ItemReceita) -> None:
        """Remove um item da receita.

        Levanta ValueError se o item não existir.
        """
        if item not in self._itens:
            raise ValueError("O item informado não pertence a esta receita.")
        self._itens.remove(item)
