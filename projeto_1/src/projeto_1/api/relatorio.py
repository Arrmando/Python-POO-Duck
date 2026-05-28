from dataclasses import dataclass
from datetime import datetime

from litestar import post
from litestar.controller import Controller
from litestar.exceptions import NotFoundException

from projeto_1.dominio.pedido import ItemPedido, Pedido
from projeto_1.dominio.relatorio import Relatorio
from projeto_1.persistencia.receita import RepositorioReceita


@dataclass
class ItemPedidoDTO:
    receita_id: int
    quantidade: float


@dataclass
class PedidoDTO:
    cliente: str
    itens: list[ItemPedidoDTO]


@dataclass
class ItemListaComprasDTO:
    insumo: str
    quantidade: float
    unidade: str
    subtotal: float


@dataclass
class RelatorioDTO:
    total_geral: float
    prazo_estimado: datetime
    lista_compras: list[ItemListaComprasDTO]

    @classmethod
    def from_relatorio(cls, relatorio: Relatorio) -> "RelatorioDTO":
        lista_compras = [
            ItemListaComprasDTO(
                insumo=item["insumo"].nome,
                quantidade=item["quantidade"],
                unidade=item["insumo"].unidade,
                subtotal=item["subtotal"],
            )
            for item in relatorio.gerar_lista_compras()
        ]
        return cls(
            total_geral=relatorio.calcular_total_geral(),
            prazo_estimado=relatorio.calcular_prazo_estimado(),
            lista_compras=lista_compras,
        )


class RelatorioController(Controller):
    path = "/relatorio"

    @post(status_code=200)
    async def gerar_relatorio(
        self, data: PedidoDTO, repo_receita: RepositorioReceita
    ) -> RelatorioDTO:
        pedido = Pedido(cliente=data.cliente)

        for item_dto in data.itens:
            receita = repo_receita.get(item_dto.receita_id)
            if not receita:
                raise NotFoundException(
                    detail=f"Receita com ID {item_dto.receita_id} não encontrada."
                )

            item_pedido = ItemPedido(receita=receita, coeficiente=item_dto.quantidade)
            pedido.adicionar_item(item_pedido)

        relatorio = Relatorio()
        relatorio.adicionar_pedido(pedido)

        return RelatorioDTO.from_relatorio(relatorio)
