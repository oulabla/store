from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_

from . import BaseRepository
from store.models.user import User

class SecurityRepository:

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
    


