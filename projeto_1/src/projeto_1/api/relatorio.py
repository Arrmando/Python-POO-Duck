from dataclasses import dataclass
from datetime import datetime

from litestar import post
from litestar.controller import Controller

from projeto_1.dominio.pedido import ItemPedido, Pedido
from projeto_1.dominio.relatorio import ItemListaCompras, Relatorio
from projeto_1.persistencia.receita import RepositorioReceita


@dataclass
class ItemPedidoDTO:
    receita_id: int
    coeficiente: float


@dataclass
class PedidoDTO:
    cliente: str
    itens: list[ItemPedidoDTO]


@dataclass
class InsumoSimplificadoDTO:
    nome: str
    unidade: str
    preco_base: float


@dataclass
class ItemListaComprasDTO:
    insumo: InsumoSimplificadoDTO
    quantidade: float
    subtotal: float

    @classmethod
    def from_dominio(cls, item: ItemListaCompras) -> "ItemListaComprasDTO":
        insumo = item["insumo"]
        return cls(
            insumo=InsumoSimplificadoDTO(
                nome=insumo.nome,
                unidade=insumo.unidade,
                preco_base=insumo.preco_base,
            ),
            quantidade=item["quantidade"],
            subtotal=item["subtotal"],
        )


@dataclass
class RelatorioDTO:
    total_geral: float
    lista_compras: list[ItemListaComprasDTO]
    prazo_estimado: datetime | None

    @classmethod
    def from_dominio(cls, relatorio: Relatorio) -> "RelatorioDTO":
        return cls(
            total_geral=relatorio.calcular_total_geral(),
            lista_compras=[
                ItemListaComprasDTO.from_dominio(item)
                for item in relatorio.gerar_lista_compras()
            ],
            prazo_estimado=relatorio.calcular_prazo_estimado(),
        )


class RelatorioController(Controller):
    path = "/relatorio"

    @post()
    async def gerar_relatorio(
        self, data: list[PedidoDTO], repositorio_receita: RepositorioReceita
    ) -> RelatorioDTO:
        relatorio = Relatorio()

        for p_dto in data:
            pedido = Pedido(cliente=p_dto.cliente)
            for i_dto in p_dto.itens:
                receita = repositorio_receita.get(i_dto.receita_id)
                if not receita:
                    msg = f"Receita com ID {i_dto.receita_id} não encontrada."
                    raise ValueError(msg)


                item_pedido = ItemPedido(receita=receita, coeficiente=i_dto.coeficiente)
                pedido.adicionar_item(item_pedido)

            relatorio.adicionar_pedido(pedido)

        return RelatorioDTO.from_dominio(relatorio)
