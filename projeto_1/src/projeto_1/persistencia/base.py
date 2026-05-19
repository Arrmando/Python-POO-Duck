from abc import ABC, abstractmethod
from typing import Any


class Repositorio(ABC):
    """Classe abstrata para definir os métodos que devem ser implementados
    pelos repositórios concretos"""

    @abstractmethod
    def save(self, entidade: Any) -> None:
        pass  ##salva uma entidade no repositório

    @abstractmethod
    def update(self, entidade: Any) -> None:
        pass  ##atualiza uma entidade no repositório

    @abstractmethod
    def get(self, id: int) -> Any:
        pass  ##busca uma entidade pelo ID

    @abstractmethod
    def list(self) -> list[Any]:
        pass  ##lista todas as entidades no repositório

    @abstractmethod
    def delete(self, id: int) -> None:
        pass  ##deleta uma entidade pelo ID