from aiohttp import web


def setup_routes(app: web.Application):

    app.container.security_controller().setup(app)
    app.container.user_controller().setup(app)
    app.container.role_controller().setup(app)
    app.container.websocket_controller().setup(app)
    app.container.employee_controller().setup(app)

    app.add_routes([
        web.get('/', app.container.index_view.as_view()),
        web.get('/health', app.container.health_controller().get),
    ])