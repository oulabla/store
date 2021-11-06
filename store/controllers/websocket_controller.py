from aiohttp import web
import aiohttp
from aiohttp_security.api import check_permission
from . import BaseJsonController
import ujson

class WebSocketController(BaseJsonController):
    ROUTE = "/ws"

    def setup(self, app: web.Application):
        app.add_routes([
            web.get(self.ROUTE, self.ws_handler),
            # web.get(self.ROUTE +'/{id}', self.get_handler),
            # web.post(self.ROUTE, self.insert_handler),
            # web.put(self.ROUTE + '/{id}', self.update_handler),
            # web.delete(self.ROUTE +'/{id}', self.delete_handler),
        ])

    async def ws_handler(self, request):
        await check_permission(request, 'observer')
        
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                reqMsg = ujson.loads(msg.data)
                
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_json({
                        "type": "test",
                        "data": {
                            "success": True,
                            "messageReq": reqMsg["message"],
                        }
                    })
            elif msg.type == aiohttp.WSMsgType.ERROR:
                 print('ws connection closed with exception %s' % ws.exception())

        return ws
