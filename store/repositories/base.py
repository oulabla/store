

import abc
import abc
from typing import Any, AsyncIterator, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from store.models import BaseModel


class BaseRepository(abc.ABC):
    
    @abc.abstractproperty
    def model(self) -> BaseModel:
        pass

    async def find(self, session: AsyncSession, id : int) -> BaseModel:
        select_query = (
            select(self.model)
            .filter_by(id=id)
        )
        result = await session.execute(select_query)
        return result.scalars().one()  

    
    async def count(self, session: AsyncSession, *filters) -> int:
        select_query = (
            select(func.count(self.model.id))
        ).filter_by(*filters)
        
        result = await session.execute(select_query)

        return result.scalar()

    async def stream_list(self, session: AsyncSession, *filters, limit:int=10, offset:int=0)  -> AsyncIterator[Any]:
        query= (
            select(
                self.model
            )
            .filter_by(*filters)
            .order_by(self.model.id)                    
            .limit(limit)
            .offset(offset)
        )
        
        data_stream = await session.stream(query)

        async for row in data_stream:
            yield row


    async def persist(self, session: AsyncSession, entity: BaseModel):
        session.add(entity)

    async def delete(self, session: AsyncSession, entity: BaseModel):
        await session.delete(entity)        