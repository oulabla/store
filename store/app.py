import asyncio
from aiohttp import web
from dependency_injector import containers
import uvloop
from aiohttp_swagger import *
import aiotask_context

from .database import DataBaseManager
from .logger import AppLogger
from .containers import ApplicationContainer
from .routes import setup_routes




def get_current_request(logger: AppLogger) -> str:
    request_id = aiotask_context.get("X-Request-ID", None)

    if request_id:
        logger.debug(f"Current request ID is: `{request_id}`.")
        return request_id

    logger.warn("Request ID is missing from the context!")


async def on_app_startup(app: web.Application):
    port = app.container.config.application.port()
    
    app.logger.info(f"Application Start on Port {port}")
    db = app.container.database()
    app.db = db
    db.initialize(scope_function=get_current_request)


async def on_app_cleanup(app: web.Application):
    app.logger.info("Cleaning up Store Application resources...")
    await app.db.cleanup()
    app.logger.info("Store Application resources were successfully cleaned up!")


async def on_app_shutdown(app: web.Application):
    app.logger.info("Shutting down example_web_app...")


def create_app() -> web.Application:
    loop = asyncio.get_event_loop()
    loop.set_task_factory(aiotask_context.task_factory)

    container = ApplicationContainer()

    app: web.Application = container.app()
    app.container = container
    container.config.from_yaml('config.yaml')

    setup_routes(app)
    setup_swagger(app, swagger_url='doc', ui_version=3)

    

    app.on_startup.append(on_app_startup)
    app.on_cleanup.append(on_app_cleanup)
    app.on_shutdown.append(on_app_shutdown)
    
    uvloop.install()

    return app

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, port=app.config.application.port, access_log=app.container.logger())