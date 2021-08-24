import asyncio
import websockets


class WebSocketServer():

    def __init__(self):
        super(WebSocketServer, self).__init__()

    async def _new_session(self, ws, path):
        rsp = await ws.recv()
        print(path, rsp)

    async def listen(self, port):

        async def call_back(ws, path):
            await self._new_session(ws, path)

        try:
            print(f"WebSocket Server listen at {port}")
            await websockets.serve(call_back, port=port)
        except Exception as error:
            print(error)


if __name__ == '__main__':
    ws = WebSocketServer()
    loop = asyncio.get_event_loop()
    loop.create_task(ws.listen(1061))
    loop.run_forever()
