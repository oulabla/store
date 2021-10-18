from store.logger import AppLogger
from aiohttp import web

from store.repositories.user_repo import UserRepository
from . import BaseJsonController

from store.logger import AppLogger
from store.database import DataBaseManager
from store.schemas.user_schema import UserSchema


class UserController(BaseJsonController):
    ROUTE = "/api/v1/users"

    def __init__(self, logger: AppLogger, user_repository: UserRepository) -> None:
        super().__init__()
        self.repo = user_repository

    def setup(self, app: web.Application):
        app.add_routes([
            web.get(self.ROUTE, app.container.user_controller().get_list),
            web.get(self.ROUTE +'/{id}', app.container.user_controller().get),
            web.post(self.ROUTE, app.container.user_controller().insert),
            web.delete(self.ROUTE +'/{id}', app.container.user_controller().delete),
        ])

    async def get_list(self, request: web.Request) -> web.Response:
        data = []
        total = 0
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                total = await self.repo.count(session)
                async for user_el in self.repo.stream_list(session):
                    data.append(user_el)

        return await self.response({
            "data": data,
            "total": total,
        })

    async def get(self, request: web.Request) -> web.Response:
        id = int(request.match_info['id'])
        user = None
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                user = await self.repo.find(session, id)

        schema = UserSchema() 
        return await self.response({
            "data": schema.dump(user),
        })


    async def insert(self, request: web.Request) -> web.Response:
        body = await request.json()    
        if "name" not in body:
            raise web.HTTPBadRequest("No field name")
    
        user = self.repo.model()
        user.name = str(body["name"])
        
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                await self.repo.persist(session, user)
        
        schema = UserSchema() 
        return await self.response({
            "data": schema.dump(user),
        })

    async def update(self, request: web.Request) -> web.Response:
        id = int(request.match_info['id'])
        
        try:
            body = await request.json()    
        except:
            raise web.HTTPBadRequest("Invalid input json")
        
        if "name" not in body:
            raise web.HTTPBadRequest("No field name")
        name = body["name"]

        additional_info = ""
        if "additionalInfo" in body:
            additional_info = body["additionalInfo"]

        roles_id_list = []
        if "roles" in body:
            for role_data in body["roles"]:
                if "id" not in role_data:
                    continue
                roles_id_list.append(role_data["id"])

        schema = UserSchema() 
        data = {}
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                user = await self.repo.find(session, id)
                data = schema.dump(user)
                
                
                session.flush()
                session.commit()
        
        
        return await self.response({
            "data": data,
        })
    


    async def delete(self, request: web.Request) -> web.Response:
        id = int(request.match_info['id'])
        
        schema = UserSchema() 
        data = {}
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                user = await self.repo.find(session, id)
                data = schema.dump(user)
                await self.repo.delete(session, user)
                
                session.flush()
                session.commit()
        
        
        return await self.response({
            "data": data,
        })
    
    
