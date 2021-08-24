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


if __name__ == '__main__':
    tcp = TcpServer()
    loop = asyncio.get_event_loop()
    loop.create_task(tcp.listen(1060))
    loop.run_forever()
