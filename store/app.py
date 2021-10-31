import base64
from cryptography import fernet
import asyncio
from aiohttp import web
from dependency_injector import containers
import uvloop
from aiohttp_swagger import *
import aiotask_context
from aiohttp_session import setup as setup_sesssion 
# , SimpleCookieStorage
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_cors

from store.authorization_policy import AuthorizationPolicy
from aiohttp_security import SessionIdentityPolicy, setup as setup_security

from .database import DataBaseManager
from .logger import AppLogger
from .containers import ApplicationContainer
from .routes import setup_routes
from .swagger_definitions import swagger_models_definitions


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
    
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup_sesssion(app, EncryptedCookieStorage(secret_key))

    cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    setup_routes(app)

    for route in list(app.router.routes()):
        cors.add(route)
    
    setup_swagger(app, 
        swagger_url='doc', 
        ui_version=3, 
        swagger_from_file="swagger_doc.yaml",
        # definitions=swagger_models_definitions,
        swagger_validator_url='//online.swagger.io/validator'
    )
    # app.router.add_static('/static', path='./static/store-app/src/', name='static')
    app.router.add_static('/static', path='./static/', name='static')

    policy = SessionIdentityPolicy()
    setup_security(app, policy, AuthorizationPolicy())


    app.on_startup.append(on_app_startup)
    app.on_cleanup.append(on_app_cleanup)
    app.on_shutdown.append(on_app_shutdown)
    
    uvloop.install()

    return app

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, port=app.config.application.port, access_log=app.container.logger())