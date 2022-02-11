from interface.iserver import IServer


class Server(IServer):

    def __init__(self, name: str, ip: str, port: int, version: str):
        super(Server, self).__init__()
        self.name = name
        self.ip = ip
        self.port = port
        self.version = version

    def server(self):
        while True:
            await self.start()

    async def start(self):
        pass

    def stop(self):
        pass


def get_new_server():
    _srv_instance = Server("pinx", "127.0.0.1", 7777, "IPv_4")
    return _srv_instance
