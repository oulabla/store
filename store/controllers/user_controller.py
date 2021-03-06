from store.logger import AppLogger
from aiohttp import web
from store.repositories.role_repo import RoleRepository

from store.repositories.user_repo import UserRepository
from store.repositories.role_repo import RoleRepository
from . import BaseJsonController

from store.logger import AppLogger
from store.schemas.user_schema import UserSchema
from store.models.phone import Phone

class UserController(BaseJsonController):
    ROUTE = "/api/v1/users"

    def __init__(self, logger: AppLogger, user_repository: UserRepository, role_repository: RoleRepository) -> None:
        super().__init__()
        self.logger = logger
        self.repo = user_repository
        self.role_repo = role_repository

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
        async with request.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                total = await self.repo.count(session)
                async for user_el in self.repo.stream_list(session):
                    data.append(user_el)

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

        schema = UserSchema() 
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
        
        schema = UserSchema() 
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
                user = await self.repo.find_one(session, id)
                user.additional_info = additional_info
                user.name = name
                
                roleModel = self.role_repo.model
                roles = await self.role_repo.find(session,  roleModel.id.in_(roles_id_list))
                user.roles.clear()
                for role in roles:
                    user.roles.append(role)

                if "phones" in body:
                    new_phones_id_list = [phone_data['id'] for phone_data in body["phones"] if 'id' in phone_data]
                    list_phones_difference = [phone for phone in user.phones if phone.id not in new_phones_id_list]
                    for phone in list_phones_difference:
                        user.phones.remove(phone)
                
                    for phone_data in body["phones"]:
                        phone = None
                        if "id" in phone_data:
                            phone = next((phone for phone in user.phones if phone.id == int(phone_data["id"])), None)
                        if phone is None:
                            phone = Phone()
                            phone.user_id = user.id
                            session.add(phone)
                            user.phones.append(phone)
                        phone.phone = phone_data["phone"]
                else:
                    user.phones.clear()

                await session.flush()
                data = schema.dump(user)
                await session.commit()
        
        
        return await self.response({
            "data": data,
        })


    async def delete_handler(self, request: web.Request) -> web.Response:
        id = int(request.match_info['id'])
        
        schema = UserSchema() 
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
    
    
