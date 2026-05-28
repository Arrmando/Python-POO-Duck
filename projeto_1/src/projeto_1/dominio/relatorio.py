from datetime import datetime, timedelta
from typing import TypedDict

from projeto_1.dominio.base import Insumo
from projeto_1.dominio.homem_hora import HomemHora
from projeto_1.dominio.pedido import Pedido


class ItemListaCompras(TypedDict):
    insumo: Insumo
    quantidade: float
    subtotal: float


class Relatorio:
    """Representa um relatório que consolida múltiplos pedidos.
    Este relatório permite gerenciar uma coleção de pedidos e realizar
    análises sobre eles, como a geração de listas de compras consolidadas
    e a estimativa de prazos baseada na carga horária necessária.
    """

    def __init__(
        self,
        pedidos: list[Pedido] | None = None,
        prazo: datetime | None = None,
    ) -> None:
        self._pedidos: list[Pedido] = pedidos if pedidos is not None else []
        self._prazo = prazo

    @property
    def pedidos(self) -> list[Pedido]:
        """Retorna uma cópia da lista de pedidos para preservar a integridade."""
        return list(self._pedidos)

    @property
    def prazo(self) -> datetime | None:
        """Retorna o prazo para entrega do relatório consolidado."""
        return self._prazo

    def adicionar_pedido(self, pedido: Pedido) -> None:
        """Adiciona um novo pedido ao relatório."""
        if not isinstance(pedido, Pedido):
            raise ValueError("Apenas objetos do tipo Pedido podem ser adicionados.")
        self._pedidos.append(pedido)

    def remover_pedido(self, pedido: Pedido) -> None:
        """Remove um pedido do relatório."""
        if pedido not in self._pedidos:
            raise ValueError("O pedido informado não pertence a este relatório.")
        self._pedidos.remove(pedido)

    def calcular_total_geral(self) -> float:
        """Calcula a soma do valor total de todos os pedidos no relatório."""
        return sum(pedido.calcular_total() for pedido in self._pedidos)

    def gerar_lista_compras(self) -> list[ItemListaCompras]:
        """Gera uma lista de compras agregando todos os insumos de todos os pedidos.
        Exclui insumos do tipo HomemHora, focando apenas em ingredientes físicos.
        Retorna uma lista de dicionários contendo o insumo, a quantidade total
        necessária e o subtotal (quantidade * preço base do insumo).
        """
        agregado: dict[int, ItemListaCompras] = {}

        for pedido in self._pedidos:
            for item_pedido in pedido.itens:
                receita = item_pedido.receita
                coeficiente_pedido = item_pedido.coeficiente

                for item_receita in receita.itens:
                    insumo = item_receita.insumo

                    # Ignora HomemHora na lista de compras
                    if isinstance(insumo, HomemHora):
                        continue

                    # A quantidade do insumo na receita é o seu coeficiente
                    qtd_na_receita = item_receita.coeficiente
                    qtd_total = qtd_na_receita * coeficiente_pedido

                    # Usando id() como fallback se o insumo não tiver ID ainda
                    insumo_id = id(insumo)

                    if insumo.id is not None:
                        insumo_id = insumo.id

                    if insumo_id in agregado:
                        agregado[insumo_id]["quantidade"] += qtd_total
                        agregado[insumo_id]["subtotal"] += qtd_total * insumo.preco_base
                    else:
                        agregado[insumo_id] = {
                            "insumo": insumo,
                            "quantidade": qtd_total,
                            "subtotal": qtd_total * insumo.preco_base,
                        }

        return list(agregado.values())

    def calcular_prazo_estimado(
        self, horas_diarias: float = 8.0, data_inicio: datetime | None = None
    ) -> datetime:
        """Calcula o prazo estimado para conclusão baseando-se no HomemHora.
        Soma todas as horas de mão de obra necessárias em todos os pedidos e
        projeta uma data de término considerando a jornada diária informada.
        """
        total_horas = 0.0
        for pedido in self._pedidos:
            for item_pedido in pedido.itens:
                for item_receita in item_pedido.receita.itens:
                    if isinstance(item_receita.insumo, HomemHora):
                        total_horas += (
                            item_receita.coeficiente * item_pedido.coeficiente
                        )

        if data_inicio is None:
            data_inicio = datetime.now()

        if total_horas == 0:
            return data_inicio

        dias_necessarios = total_horas / horas_diarias
        return data_inicio + timedelta(days=dias_necessarios)
