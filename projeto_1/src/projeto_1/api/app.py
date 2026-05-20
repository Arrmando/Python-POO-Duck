from litestar import Litestar
from litestar.di import Provide

from projeto_1.api.insumo import InsumoController
from projeto_1.api.status import StatusController
from projeto_1.persistencia.insumo import RepositorioInsumo


def make_app(repositorio: RepositorioInsumo | None = None) -> Litestar:
    if repositorio is None:
        repositorio = RepositorioInsumo()
    return Litestar(
        route_handlers=[StatusController, InsumoController],
        dependencies={
            "repositorio": Provide(lambda: repositorio, sync_to_thread=False)
        },
    )


app = make_app()
