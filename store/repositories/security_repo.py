from typing import AsyncIterator, List
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_

from . import BaseRepository
from store.models.user import User
from store.models.role import Role

class SecurityRepository:

    async def get_roles(self, session: AsyncSession, user_id: int) -> List[str]:
        select_query  = (
            select(Role.name)
            .select_from(Role)
            .join(Role, User.roles)
            .where(User.id==user_id)            
        )
        data_stream = await session.stream(select_query)
        roles = []
        async for row in data_stream:
            roles.append(row[0])
        return roles

    async def login(self, session: AsyncSession, username: str, password: str) -> User:
        select_query = (
            select(User)
            .options(
                selectinload(User.roles), 
                selectinload(User.phones)
            )
            .where(and_(User.username==username, User.password==password))
            # .filter_by(and_(User.username==username, User.password==password))
        )
        result = await session.execute(select_query)
        
        return result.scalars().one()        
    


