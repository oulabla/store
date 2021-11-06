from __future__ import annotations
import aiohttp
from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp
from aiohttp import web

from store.controllers import ( 
    health_controller, 
    user_controller, 
    role_controller,
    security_controller,    
    websocket_controller,
    employee_controller,
)

from store.repositories import security_repo, user_repo, role_repo, employee_repo

from .logger import AppLogger
from .database import DataBaseManager

from store.middlewares import request_context_middleware
from store.views import index_view



class ApplicationContainer(containers.DeclarativeContainer):
    container: ApplicationContainer = None

    config = providers.Configuration()

    logger = providers.Factory(AppLogger, name=config.application.name)
    database = providers.Factory(DataBaseManager, logger=logger, conn_url=config.database.url)
    
    app = aiohttp.Application(web.Application, logger=logger, middlewares=[
        request_context_middleware
    ])

    user_repository = providers.Factory(user_repo.UserRepository)
    role_repository = providers.Factory(role_repo.RoleRepository)
    security_repository = providers.Factory(security_repo.SecurityRepository)
    employee_repository = providers.Factory(employee_repo.EmployeeRepository)
    

    health_controller = providers.Factory(health_controller.HealthController)
    security_controller = providers.Factory(security_controller.SecurityController, logger=logger, security_repository=security_repository)
    user_controller = providers.Factory(user_controller.UserController, logger=logger, user_repository=user_repository, role_repository=role_repository)
    role_controller = providers.Factory(role_controller.RoleController, logger=logger, role_repository=role_repository)
    websocket_controller = providers.Factory(websocket_controller.WebSocketController)
    employee_controller = providers.Factory(employee_controller.EmployeeController, logger=logger, employee_repository=employee_repository)

    index_view = aiohttp.View(index_view, logger=logger)