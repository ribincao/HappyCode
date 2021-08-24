import websockets
import asyncio


class TcpServer():

    def __init__(self):
        super(TcpServer, self).__init__()

    async def _new_session(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        pass

    async def listen(self, port):

        async def call_back(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
            await self._new_session(reader, writer)

        try:
            print(f"Tcp Server listen at {port}")
            await asyncio.start_server(call_back, port=port)
        except Exception as error:
            print(error)

class WebSocketServer():

    def __init__(self):
        super(WebSocketServer, self).__init__()

    async def _new_session(self, ws, path):
        while True:
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

class Gateway():

    def __init__(self):
        super(Gateway, self).__init__()
        self._loop = asyncio.get_event_loop()
        self._tcp_server = TcpServer()
        self._web_socket_server = WebSocketServer()

    def run(self):
        socket_port, web_socket_port = 1060, 1061
        # self._loop.create_task(self.socket_listen(socket_port))
        self._loop.create_task(self.web_socket_listen(web_socket_port))

        self._loop.run_forever()
    
    async def socket_listen(self, port: int):
        await self._tcp_server.listen(port)

    async def web_socket_listen(self, port: int):
        await self._web_socket_server.listen(port)


if __name__ == '__main__':
    gw = Gateway()
    gw.run()
