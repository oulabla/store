import random
from aiohttp import web

from . import BaseJsonController

class HealthController(BaseJsonController):
    
    async def get(self, request: web.Request):

        return await self.response(body={
            "status": "Ok",
            "success": True,            
        })