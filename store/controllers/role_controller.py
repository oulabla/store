from store.logger import AppLogger
from aiohttp import web
from store.repositories.role_repo import RoleRepository

from store.repositories.role_repo import RoleRepository
from . import BaseJsonController

from store.logger import AppLogger
from store.schemas.role_schema import RoleSchema
from store.models.phone import Phone

class RoleController(BaseJsonController):
    ROUTE = "/api/v1/roles"

    def __init__(self, logger: AppLogger, role_repository: RoleRepository) -> None:
        super().__init__()
        self.logger = logger
        self.repo = role_repository

    def setup(self, app: web.Application):
        app.add_routes([
            web.get(self.ROUTE, self.get_list_handler),
            web.get(self.ROUTE +'/{id}', self.get_handler),
            web.post(self.ROUTE, self.insert_handler),
            web.put(self.ROUTE + '/{id}', self.update_handler),
            web.delete(self.ROUTE +'/{id}', self.delete_handler),
        ])

    async def get_list_handler(self, request: web.Request) -> web.Response:
        data = []
        total = 0
        schema = RoleSchema()
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                total = await self.repo.count(session)
                async for role in self.repo.stream_list(session):
                    data.append(schema.dump(role))

        return await self.response({
            "data": data,
            "total": total,
        })

    async def get_handler(self, request: web.Request) -> web.Response:
        id = int(request.match_info['id'])
        user = None
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                user = await self.repo.find_one(session, id)

        schema = RoleSchema() 
        return await self.response({
            "data": schema.dump(user),
        })


    async def insert_handler(self, request: web.Request) -> web.Response:
        body = await request.json()    
        if "name" not in body:
            raise web.HTTPBadRequest("No field name")
    
        user = self.repo.model()
        user.name = str(body["name"])
        
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                await self.repo.persist(session, user)
        
        schema = RoleSchema() 
        return await self.response({
            "data": schema.dump(user),
        })

    async def update_handler(self, request: web.Request) -> web.Response:
        id = int(request.match_info['id'])
        
        try:
            body = await request.json()    
        except:
            raise web.HTTPBadRequest("Invalid input json")
        
        if "name" not in body:
            raise web.HTTPBadRequest("No field name")
        name = body["name"]

        schema = RoleSchema() 
        data = {}
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                role = await self.repo.find_one(session, id)
                role.name = name
                await session.flush()
                data = schema.dump(role)
                await session.commit()
        
        
        return await self.response({
            "data": data,
        })


    async def delete_handler(self, request: web.Request) -> web.Response:
        id = int(request.match_info['id'])
        
        schema = RoleSchema() 
        data = {}
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                user = await self.repo.find_one(session, id)
                data = schema.dump(user)
                await self.repo.delete(session, user)
                
                session.flush()
                session.commit()
        
        
        return await self.response({
            "data": data,
        })
    
    
