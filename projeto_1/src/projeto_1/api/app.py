from litestar import Litestar

from projeto_1.api.status import StatusController

app = Litestar(route_handlers=[StatusController])
