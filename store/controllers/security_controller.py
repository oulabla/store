from aiohttp import web
from aiohttp_security.api import check_permission
from sqlalchemy.orm.exc import NoResultFound
from store import schemas
from aiohttp_security import remember

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
            web.get(self.ROUTE + '/login2', self.login2_handler),
            web.get(self.ROUTE + '/test', self.login_test),
        ])

    async def login_test(self, request: web.Request) -> web.Response:
        await check_permission(request, 'observer')

        return web.json_response({
            "success": True,
        })

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
        
        await remember(request, web.json_response({
            "success": True,
            "data": UserSchema().dump(user)
        }), str(user.id))
        
        return web.json_response({
        "success": True,
        "data": UserSchema().dump(user)
        })

    async def login2_handler(self, request: web.Request) -> web.Response:
        username = ""
        if "username" in request.rel_url.query:
            username = str(request.rel_url.query["username"])

        password = ""
        if "password" in request.rel_url.query:
            password = str(request.rel_url.query["password"])
        
        print(f'username: {username} password: {password}')

        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                try:
                    user = await self.repo.login(session, username, password)
                except NoResultFound:
                    raise web.HTTPNotFound()
        
        await remember(request, web.json_response({
            "success": True,
            "data": UserSchema().dump(user)
        }), str(user.id))

        return web.json_response({
            "success": True,
            "data": UserSchema().dump(user)
        })
