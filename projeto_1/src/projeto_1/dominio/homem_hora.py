from projeto_1.dominio.base import Insumo


class HomemHora(Insumo):
    # Atributo de classe: compartilhado por todas as instâncias
    _unidade: str = "h"

    def __init__(
        self,
        nome: str,
        quantidade: int,
        preco_base: float,
        id: int = None,
    ):
        super().__init__()
        self._id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco_base = preco_base

    @property
    def id(self):
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "O nome do HomemHora deve ser uma string não vazia "
                "contendo o nome do profissional ou função."
            )
        self._nome = valor

    @property
    def unidade(self) -> str:
        return self._unidade

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError(
                "A quantidade do HomemHora deve ser um inteiro maior que zero."
            )
        self._quantidade = valor

    @property
    def preco_base(self) -> float:
        return self._preco_base

    @preco_base.setter
    def preco_base(self, valor: float):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError(
                "O preço base do HomemHora deve ser um número não negativo."
            )
        self._preco_base = valor

    def calcular_total(self) -> float:
        return self.preco_base * self.quantidade

    def __str__(self) -> str:
        return (
            f"{self.nome}: {self.quantidade}{self.unidade} x "
            f"R$ {self.preco_base:.2f}/{self.unidade} = "
            f"R$ {self.calcular_total():.2f}"
        )
