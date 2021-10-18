from __future__ import annotations
import aiohttp
from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp
from aiohttp import web

from store import middlewares
from store.controllers import health_controller, user_controller
from store.repositories import user_repo
from store.repositories import role_repo
from store.repositories.role_repo import RoleRepository

from .logger import AppLogger
from .database import DataBaseManager

from store.middlewares import request_context_middleware
from store.views import index_view

from store.controllers import HealthController


class ApplicationContainer(containers.DeclarativeContainer):
    container: ApplicationContainer = None
    

    config = providers.Configuration()

    logger = providers.Factory(AppLogger, name=config.application.name)
    database = providers.Factory(DataBaseManager, logger=logger, conn_url=config.database.url)
    
    app = aiohttp.Application(web.Application, logger=logger, middlewares=[
        request_context_middleware
    ])

    user_repository = providers.Factory(user_repo.UserRepository)
    role_repository = providers.Factory(RoleRepository)

    health_controller = providers.Factory(health_controller.HealthController)
    user_controller = providers.Factory(user_controller.UserController, logger=logger, user_repository=user_repository, role_repository=role_repository)

    index_view = aiohttp.View(index_view, logger=logger)