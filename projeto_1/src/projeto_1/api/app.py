from litestar import Litestar, Request, Response
from litestar.di import Provide
from litestar.status_codes import HTTP_400_BAD_REQUEST

from projeto_1.api.insumo import InsumoController
from projeto_1.api.status import StatusController
from projeto_1.persistencia.insumo import RepositorioInsumo


def _value_error_handler(_: Request, exc: ValueError) -> Response:
    return Response({"detail": str(exc)}, status_code=HTTP_400_BAD_REQUEST)


def make_app(repositorio: RepositorioInsumo | None = None) -> Litestar:
    if repositorio is None:
        repositorio = RepositorioInsumo()
    return Litestar(
        route_handlers=[StatusController, InsumoController],
        dependencies={
            "repositorio": Provide(lambda: repositorio, sync_to_thread=False)
        },
        exception_handlers={ValueError: _value_error_handler},
    )


app = make_app()
