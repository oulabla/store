from aiohttp import web
from sqlalchemy.orm.exc import NoResultFound
from store import schemas

from store.repositories.security_repo import SecurityRepository
from . import BaseJsonController
from store.logger import AppLogger
from store.schemas.user_schema import UserSchema


class SecurityController(BaseJsonController):
    ROUTE = '/security'

    def __init__(self, logger: AppLogger, security_repository: SecurityRepository):
        super().__init__()
        self.logger = logger
        self.repo = security_repository

    def setup(self, app: web.Application):
        app.add_routes([
            web.post(self.ROUTE + '/login', self.login_handler),
        ])

    async def login_handler(self, request: web.Request) -> web.Response:
        body = await request.json()    
        if "username" not in body:
            raise web.HTTPBadRequest("No field username")
    
        if "password" not in body:
            raise web.HTTPBadRequest("No field password")
    
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                try:
                    user = await self.repo.login(session, body["username"], body["password"])
                except NoResultFound:
                    raise web.HTTPNotFound()
        
        return web.json_response({
            "success": True,
            "data": UserSchema().dump(user)
        })
