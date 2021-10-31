from aiohttp import web
from aiohttp_security.abc import AbstractAuthorizationPolicy
from store.repositories.security_repo import SecurityRepository

class AuthorizationPolicy(AbstractAuthorizationPolicy):
    
    def __init__(self, app: web.Application) -> None:
        self.app = app
        super().__init__()

    async def authorized_userid(self, identity):
        return identity


    async def permits(self, identity, permission, context=None):
        repo = SecurityRepository()
        async with self.app.db.AsyncSessionFactory() as session:
            async with session.begin():
                roles = await repo.get_roles(session, int(identity))
        if permission in roles:
            return True
        return False