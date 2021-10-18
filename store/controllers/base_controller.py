from typing import Any, Dict, List
import asyncio
from concurrent.futures import ThreadPoolExecutor
from aiohttp.web_response import Response
import ujson
from aiohttp import web

class BaseJsonController:

    STATUS_MESSAGES = {
        200: 'OK',
        201: 'Created',
        207: 'Mixed status',
        400: 'Invalid {model} resource representation',
        401: 'Unauthorized request.',
        404: 'The requested resource was not found.',
        405: 'Method not allowed.',
        409: 'Another resource exists with the same <id or unique field>.',
        500: 'An error occurred while processing your request, please retry!',
        520: 'Unknown error.'
    }

    def setup(app: web.Application):
        pass
    
    @classmethod
    async def response(cls, body: Any = None, status: int = 200, reason : str = None, headers: Dict[str, Any] = None) -> web.Response:
        loop = asyncio.get_running_loop()
        stringify_future = loop.run_in_executor(None, ujson.dumps, body)
        json_body = await stringify_future

        return web.Response(
            text=json_body,
            status=status,
            reason=reason,
            headers=headers,
            charset="utf-8",
            content_type="application/json")

    
    @classmethod
    async def error(cls, status: int, reason: str = None, errors: List[Dict[str, str]]=None, headers: Dict[str, Any]=None) -> web.Response:
        body = {
            'message' : reason or cls.STATUS_MESSAGES.get(status, '')
        }

        if errors:
            body['errors'] = errors

        return await cls.response(body=body, status=status, headers=headers)
    