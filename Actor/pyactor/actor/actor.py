from abc import ABC
from asyncio import Queue
from typing import Optional, TypeVar


class ActorInterface(ABC):
    pass


ActorInterfaceType = TypeVar("ActorInterfaceType", bound=ActorInterface)


class ActorContext(object):

    def __init__(self):
        self.__mail_box = Queue()
        self.reentrant_id = 0


class ActorBase(ActorInterface, ABC):

    def __init__(self):
        self.__uid = 0
        self.__context: Optional[ActorContext]

    def get_proxy(self):
        # todo: get rpc proxy
        pass
