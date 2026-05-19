from typing import Any

from src.projeto_1.dominio.base import Insumo
from src.projeto_1.persistencia.base import Repositorio


class RepositorioInsumo(Repositorio):
    """Repositório concreto para gerenciar os insumos, implementando os métodos
    definidos na classe abstrata Repositorio"""

    def __init__(self) -> None:
        # inicializa o dicionario vazio que funcionara como o banco de dados
        # a chave do dicionário será o ID do insumo e o valor será o objeto Insumo
        # correspondente
        self._dados: dict[Any, Insumo] = {}

    def save(self, entity: Insumo) -> None:
        """Salva um insumo no repositório, usando o ID do insumo como chave no
        dicionário"""
        if entity.id is None:
            raise ValueError("Não é possível salvar um insumo sem ID.")
        if entity.id in self._dados:
            raise ValueError(f"Já existe um insumo com ID {entity.id}.")
        self._dados[entity.id] = entity

    def update(self, entity: Insumo) -> None:
        """Atualiza um insumo existente no repositório, verificando se o ID do insumo
        existe no dicionário"""
        if entity.id is None:
            raise ValueError("Não é possível atualizar um insumo sem ID.")
        if entity.id not in self._dados:
            raise ValueError(f"Não existe um insumo com ID {entity.id} para atualizar.")
        self._dados[entity.id] = entity

    def get(self, id: Any) -> Insumo | None:
        """Recupera um insumo pelo ID. Retorna None se não existir."""
        return self._dados.get(id)

    def list(self) -> list[Insumo]:
        """Retorna uma lista com todos os insumos no repositório"""
        return list(self._dados.values())

    def delete(self, id: int) -> None:
        """Remove um insumo do repositório pelo ID, lançando um erro se o ID
        não existir"""
        if id not in self._dados:
            raise ValueError(f"Não existe um insumo com ID {id} para remover.")
        del self._dados[id]
