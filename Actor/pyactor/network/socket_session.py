from abc import abstractmethod


class SocketSession:
    @property
    @abstractmethod
    def session_id(self) -> int:
        pass

    @abstractmethod
    async def send_message(self, msg: object) -> None:
        pass