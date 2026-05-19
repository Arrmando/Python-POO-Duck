from litestar import get
from litestar.controller import Controller


class StatusController(Controller):
    path = "/status"

    @get()
    async def get_status(self) -> dict[str, str]:
        return {"status": "ok"}
