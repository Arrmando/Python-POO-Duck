from litestar import Litestar, Request, Response
from litestar.di import Provide
from litestar.status_codes import HTTP_400_BAD_REQUEST

from projeto_1.api.insumo import InsumoController
from projeto_1.api.relatorio import RelatorioController
from projeto_1.api.status import StatusController
from projeto_1.persistencia.insumo import RepositorioInsumo
from projeto_1.persistencia.receita import RepositorioReceita


def _value_error_handler(_: Request, exc: ValueError) -> Response:
    return Response({"detail": str(exc)}, status_code=HTTP_400_BAD_REQUEST)


def make_app(
    repositorio_insumo: RepositorioInsumo | None = None,
    repositorio_receita: RepositorioReceita | None = None,
) -> Litestar:
    if repositorio_insumo is None:
        repositorio_insumo = RepositorioInsumo()
    if repositorio_receita is None:
        repositorio_receita = RepositorioReceita()

    return Litestar(
        route_handlers=[StatusController, InsumoController, RelatorioController],
        dependencies={
            "repositorio": Provide(lambda: repositorio_insumo, sync_to_thread=False),
            "repo_receita": Provide(lambda: repositorio_receita, sync_to_thread=False),
        },
        exception_handlers={ValueError: _value_error_handler},
    )


app = make_app()
