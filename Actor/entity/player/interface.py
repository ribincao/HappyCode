from abc import abstractmethod


class IPlayer:
    @abstractmethod
    async def play(self):
        pass

    @abstractmethod
    async def echo(self):
        pass
