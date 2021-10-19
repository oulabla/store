import abc
from typing import Any, AsyncIterator, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from store.models import BaseModel


class BaseRepository(abc.ABC):
    
    @abc.abstractproperty
    def model(self) -> BaseModel:
        pass

    async def find_one(self, session: AsyncSession, id : int) -> BaseModel:
        select_query = (
            select(self.model)
            .filter_by(id=id)
        )
        result = await session.execute(select_query)
        return result.scalars().one()  


    async def find(self, session: AsyncSession, filter = None) -> List[BaseModel]:
        if filter == None:
            filter = 1==1
        select_query = (
            select(self.model)
            .filter(filter)
        )
        result = await session.execute(select_query)
        return result.scalars().all()

    
    async def count(self, session: AsyncSession, filter = None) -> int:
        if filter == None:
            filter = 1==1        
        select_query = (
            select(func.count(self.model.id))
        ).filter(filter)
        
        result = await session.execute(select_query)

        return result.scalar()

    async def stream_list(self, session: AsyncSession, filter=None, limit:int=10, offset:int=0)  -> AsyncIterator[Any]:
        if filter == None:
            filter = 1==1
        query= (
            select(
                self.model
            )
            .filter(filter)
            .order_by(self.model.id)                    
            .limit(limit)
            .offset(offset)
        )
        
        data_stream = await session.stream(query)

        async for row in data_stream:
            yield row[0]


    async def persist(self, session: AsyncSession, entity: BaseModel):
        session.add(entity)

    async def delete(self, session: AsyncSession, entity: BaseModel):
        await session.delete(entity)        