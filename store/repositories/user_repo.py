from typing import Any, Dict, AsyncIterator

from . import BaseRepository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from store.models.user import User
from store.models.role import Role
from store.models.phone import Phone

class UserRepository(BaseRepository):

    @property
    def model(self) -> User:
        return User

    async def stream_list(self, session: AsyncSession, *filters, limit=10, offset=0) -> AsyncIterator[Dict[str, Any]]:
        query= (
            select(
                User.id, 
                User.name,
                func.to_char(User.created_at, 'YYYY-MM-DD HH:MI:SS').label("createdAt"),
                func.coalesce(func.string_agg(Role.name.distinct(), ', '), '').label('roles'),
                func.coalesce(func.string_agg(Phone.phone.distinct(), ', '), '').label('phones'),
            ).select_from(User)
            .outerjoin(Role, User.roles)
            .outerjoin(Phone, User.phones)
            .filter_by(*filters)
            .order_by(User.id)                    
            .limit(limit)
            .offset(offset)
            .group_by(User.id)
        )

        data_stream = await session.stream(query)

        async for row in data_stream:
            record = {}
            for field_name in row.keys():
                record[field_name] = row[field_name]
            yield record


    async def find_one(self, session: AsyncSession, id : int) -> User:
        select_query = (
            select(User)
            .options(
                selectinload(User.roles), 
                selectinload(User.phones)
            )
            .filter_by(id=id)
        )
        result = await session.execute(select_query)
        return result.scalars().one()        


    # async def count(self, session: AsyncSession, *filters) -> int:
    #     select_query = (
    #         select(func.count(User.id))
    #     ).filter_by(*filters)
        
    #     result = await session.execute(select_query)

    #     return result.scalar()
