from typing import Callable
import uuid
from aiohttp import web
import aiotask_context

@web.middleware
async def request_context_middleware(request : web.Request, handler: Callable):
    x_request_header = "X-Request-Id"
    x_request = request.headers.get(x_request_header, str(uuid.uuid4()))
    aiotask_context.set(x_request_header, x_request)
    respose = await handler(request)
    respose.headers[x_request_header] = aiotask_context.get(x_request_header)

    return respose