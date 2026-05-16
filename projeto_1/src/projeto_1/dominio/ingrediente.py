from src.projeto_1.dominio.base import Insumo

class Ingrediente(Insumo):
    def __init__(self, id: int, nome: str, unidade: str, quantidade: int, preco_base: float):
        self._id = id
        self._nome = nome
        self._unidade = unidade
        self._quantidade = quantidade
        self._preco_base = preco_base

    @property
    def id(self):
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome do ingrediente deve ser uma string não vazia.")
        self._nome = valor

    @property
    def unidade(self) -> str:
        return self._unidade

    @unidade.setter    
    def unidade(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ValueError("A unidade do ingrediente deve ser uma string não vazia.")
        self._unidade = valor

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("A quantidade do ingrediente deve ser um inteiro não negativo.")
        self._quantidade = valor

    @property
    def preco_base(self) -> float:
        return self._preco_base

    @preco_base.setter
    def preco_base(self, valor: float):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("O preço base do ingrediente deve ser um número não negativo.")
        self._preco_base = valor

    def calcular_total(self) -> float:
        return self.preco_base * self.quantidade

    def __str__(self) -> str:
        return (f"Ingrediente(id={self.id}, nome='{self.nome}', unidade='{self.unidade}', "
                f"quantidade={self.quantidade}, preco_un={self.preco_base:.2f}, total={self.calcular_total():.2f})")