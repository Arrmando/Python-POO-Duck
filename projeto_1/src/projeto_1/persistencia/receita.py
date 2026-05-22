from typing import Any

from src.projeto_1.dominio.receita import Receita
from src.projeto_1.persistencia.base import Repositorio


class RepositorioReceita(Repositorio):
    """Implementação concreta de Repositorio para entidades Receita em memória com
    ID incremental."""

    def __init__(self) -> None:
        self._dados: dict[int, Receita] = {}
        self._proximo_id = 1

    def save(self, entity: Receita) -> None:
        """Salva uma nova receita gerando um ID incremental automaticamente."""
        if entity.id is not None:
            raise ValueError(
                "Não é possível salvar uma receita com ID já definido, "
                "ele já é gerado pelo repositório."
            )

        # Injeta o ID incremental diretamente no atributo privado da Receita
        setattr(entity, "_id", self._proximo_id)

        self._dados[self._proximo_id] = entity
        self._proximo_id += 1

    def update(self, entity: Receita) -> None:
        """Atualiza uma receita existente."""
        if entity.id is None:
            raise ValueError("Não é possível atualizar uma receita sem ID.")
        if entity.id not in self._dados:
            raise ValueError(
                f"Não existe uma receita com ID {entity.id} para atualizar."
            )
        self._dados[entity.id] = entity

    def get(self, id: Any) -> Receita | None:
        """Recupera uma receita pelo ID. Retorna None se não existir."""
        return self._dados.get(id)

    def list(self) -> list[Receita]:
        """Retorna uma lista com todas as receitas armazenadas."""
        return list(self._dados.values())

    def delete(self, id: int) -> None:
        """Remove uma receita pelo ID."""
        if id not in self._dados:
            raise ValueError(f"Não existe uma receita com ID {id} para remover.")
        del self._dados[id]
