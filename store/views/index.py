from aiohttp import web

from store.logger import AppLogger

async def index_view(request: web.Request, logger: AppLogger) -> web.Response:
    """
    Optional route description
    ---
    summary: This is index page
    tags:
      - index
    responses:
      '200':
        description: Expected response to a valid request
        content:
          application/json:
    """

    logger.info("index action")
    return web.json_response(
        {
            "success": True,
        }
    )