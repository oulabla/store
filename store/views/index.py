from aiohttp import web
import time
import datetime

from store.logger import AppLogger
from aiohttp_session import get_session

async def index_view(request: web.Request, logger: AppLogger) -> web.Response:
    user_session = await get_session(request)
    
    text = ''
    if 'last_visit' in user_session:
      text += 'Last visited: {}'.format(datetime.datetime.fromtimestamp(user_session['last_visit']))

    user_session['last_visit'] = time.time()
    text += '\nNow visited: {}'.format(datetime.datetime.fromtimestamp(user_session['last_visit']))


    logger.info("index action")
    return web.json_response(
        {
            "success": True,
            "text": text,
        }
    )