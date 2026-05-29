from dataclasses import dataclass

from litestar import get, post
from litestar.controller import Controller

from projeto_1.dominio.base import Insumo
from projeto_1.dominio.homem_hora import HomemHora
from projeto_1.dominio.ingrediente import Ingrediente
from projeto_1.persistencia.insumo import RepositorioInsumo


@dataclass
class CriarInsumoDTO:
    tipo: str
    nome: str
    quantidade: int
    preco_base: float
    unidade: str = ""


@dataclass
class InsumoDTO:
    id: int
    tipo: str
    nome: str
    unidade: str
    quantidade: int
    preco_base: float

    @classmethod
    def from_insumo(cls, insumo: Insumo) -> "InsumoDTO":
        return cls(
            id=insumo.id,
            tipo=type(insumo).__name__,
            nome=insumo.nome,
            unidade=insumo.unidade,
            quantidade=insumo.quantidade,
            preco_base=insumo.preco_base,
        )


class InsumoController(Controller):
    path = "/insumo"

    @get()
    # MUDANÇA AQUI: de 'repositorio' para 'repositorio_insumo'
    async def get_insumos(
        self, repositorio_insumo: RepositorioInsumo
    ) -> list[InsumoDTO]:
        return [InsumoDTO.from_insumo(i) for i in repositorio_insumo.list()]

    @post(status_code=201)
    # MUDANÇA AQUI: de 'repositorio' para 'repositorio_insumo'
    async def post_insumo(
        self, data: CriarInsumoDTO, repositorio_insumo: RepositorioInsumo
    ) -> InsumoDTO:
        if data.tipo == "Ingrediente":
            insumo = Ingrediente(
                data.nome, data.unidade, data.quantidade, data.preco_base
            )
        elif data.tipo == "HomemHora":
            insumo = HomemHora(data.nome, data.quantidade, data.preco_base)
        else:
            raise ValueError(f"Tipo desconhecido: {data.tipo}")

        repositorio_insumo.save(insumo)
        return InsumoDTO.from_insumo(insumo)
