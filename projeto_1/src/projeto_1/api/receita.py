from dataclasses import dataclass

from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.status_codes import HTTP_201_CREATED

from projeto_1.dominio.receita import Receita
from projeto_1.persistencia.receita import RepositorioReceita


@dataclass
class ReceitaDTO:
    """Classe auxiliar (DTO) para ler os dados do corpo da requisição."""

    nome: str
    instrucoes: str


class ReceitaController(Controller):
    """Controller HTTP que expõe as rotas de CRUD para a entidade Receita."""

    path = "/receitas"

    @get()
    async def list_receitas(
        self, repositorio_receita: RepositorioReceita
    ) -> list[dict]:
        """GET /receitas -> Retorna a lista de todas as receitas."""
        receitas = repositorio_receita.list()
        return [
            {"id": r.id, "nome": r.nome, "instrucoes": r.instrucoes} for r in receitas
        ]

    @post(status_code=HTTP_201_CREATED)
    async def create_receita(
        self, data: ReceitaDTO, repositorio_receita: RepositorioReceita
    ) -> dict:
        """POST /receitas -> Cria uma nova receita."""
        nova_receita = Receita(nome=data.nome, instrucoes=data.instrucoes)
        repositorio_receita.save(nova_receita)

        todas = repositorio_receita.list()
        receita_salva = todas[-1]

        return {
            "id": receita_salva.id,
            "nome": receita_salva.nome,
            "instrucoes": receita_salva.instrucoes,
        }

    @get("/{id:int}")
    async def get_receita(
        self, id: int, repositorio_receita: RepositorioReceita
    ) -> dict:
        """GET /receitas/{id} -> Recupera uma receita específica."""
        try:
            receita = repositorio_receita.get(id)
        except ValueError:
            raise NotFoundException(f"Receita com ID {id} não encontrada.")

        if receita is None:
            raise NotFoundException(f"Receita com ID {id} não encontrada.")

        return {
            "id": receita.id,  # Corrigido aqui! Sem caracteres intrusos
            "nome": receita.nome,
            "instrucoes": receita.instrucoes,
        }

    @put("/{id:int}")
    async def update_receita(
        self,
        id: int,
        data: ReceitaDTO,
        repositorio_receita: RepositorioReceita,
    ) -> dict:
        """PUT /receitas/{id} -> Atualiza os dados de uma receita."""
        try:
            receita_existente = repositorio_receita.get(id)
        except ValueError:
            raise NotFoundException(f"Receita com ID {id} não encontrada.")

        if not receita_existente:
            raise NotFoundException(f"Receita com ID {id} não encontrada.")

        receita_atualizada = Receita(id=id, nome=data.nome, instrucoes=data.instrucoes)

        try:
            repositorio_receita.update(receita_atualizada)
        except ValueError:
            raise NotFoundException(f"Receita com ID {id} não encontrada.")

        return {"id": id, "nome": data.nome, "instrucoes": data.instrucoes}

    @delete("/{id:int}")
    async def delete_receita(
        self, id: int, repositorio_receita: RepositorioReceita
    ) -> None:
        """DELETE /receitas/{id} -> Remove uma receita do sistema."""
        try:
            repositorio_receita.delete(id)
        except ValueError:
            # Comentário encurtado para evitar o erro E501 do Ruff
            raise NotFoundException(f"Receita com ID {id} não encontrada.")
