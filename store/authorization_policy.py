from aiohttp_security.abc import AbstractAuthorizationPolicy


class AuthorizationPolicy(AbstractAuthorizationPolicy):
    
    async def authorized_userid(self, identity):
        return await super().authorized_userid(identity)

    async def permits(self, identity, permission, context=None):
        return await super().permits(identity, permission, context=context)