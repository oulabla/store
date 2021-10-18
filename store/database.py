from __future__ import annotations
from typing import Callable
import importlib.util
from pathlib import Path
import os

from sqlalchemy.schema import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from store.models import BaseModel

from .logger import AppLogger

class DatabaseNotInitialized(Exception):
    def __init__(self, *args, **kwargs):
        super(DatabaseNotInitialized, self).__init__(args, kwargs)


class DataBaseManager:

    def __init__(self, conn_url : str, logger: AppLogger) -> None:
        self._conn_url = conn_url
        self._engine = None
        # self.metadata = MetaData()
        self.Session = None
        self.OnCommitExpiringSession = None
        self.AsyncSessionFactory = None
        self.BaseModel = BaseModel

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    
    def create_engine(self) -> AsyncEngine:
        engine = create_async_engine(self._conn_url, echo=True)
        return engine
    
    def initialize(self, engine: AsyncEngine = None, scope_function: Callable = None):
        if self._engine is None:
            self._engine = self.create_engine()
        else:
            self._engine = engine

        # print("initialized")
        self.AsyncSessionFactory = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )
        # print(self.AsyncSessionFactory)

        self.Session = scoped_session(
            sessionmaker(bind=self._engine, expire_on_commit=False),
            scopefunc=scope_function)

        self.OnCommitExpiringSession = scoped_session(
            sessionmaker(bind=self._engine, expire_on_commit=True),
            scopefunc=scope_function)
        
        import_all_models()
    

    async def cleanup(self):
        if self._engine is not None:
            await self._engine.dispose()


def import_all_models():
      for full_module_name in _package_contents('store.models'):
        importlib.import_module(full_module_name)

def _package_contents(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return set()

    pathname = Path(spec.origin).parent
    ret = set()
    with os.scandir(pathname) as entries:
        for entry in entries:
            if entry.name.startswith('__'):
                continue
            current = '.'.join((package_name, entry.name.partition('.')[0]))
            if entry.is_file():
                if entry.name.endswith('.py'):
                    ret.add(current)
            elif entry.is_dir():
                ret.add(current)
                ret |= _package_contents(current)

    return ret