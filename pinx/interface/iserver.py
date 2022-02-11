

class IServer:

    def __init__(self):
        pass

    def server(self):
        raise NotImplemented()

    async def start(self):
        raise NotImplemented()

    def stop(self):
        raise NotImplemented()
