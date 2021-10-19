from aiohttp import web



def setup_routes(app: web.Application):

    app.container.user_controller().setup(app)
    app.container.role_controller().setup(app)

    app.add_routes([
        web.get('/', app.container.index_view.as_view()),

        web.get('/health', app.container.health_controller().get),
        
        
        # web.get('/api/v1/users', app.container.user_controller().get_list),
        # web.get('/api/v1/users/{id}', app.container.user_controller().get),
        # web.post('/api/v1/users', app.container.user_controller().insert),
    ])