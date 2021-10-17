from store.logger import AppLogger
from aiohttp import web
from . import BaseJsonController

from store.logger import AppLogger

class UserController(BaseJsonController):
    
    def __init__(self, logger: AppLogger) -> None:
        super().__init__()

    async def get_list(self, request: web.Request) -> web.Response:
        data = []

        return await self.response({
            "data": data,
            "total": len(data),
        })
