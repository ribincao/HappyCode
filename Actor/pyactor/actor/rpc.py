import asyncio
import weakref
import pickle
from actor import *
from typing import Type, Union, cast, Any
from placement import *
from dataclasses import dataclass
import lz4.frame
from asyncio.futures import Future
ActorId = Union[int, str]


RPC_ERROR_BEGIN = 10000
RPC_ERROR_INTERFACE_INVALID = RPC_ERROR_BEGIN + 1
RPC_ERROR_IMPL_INVALID = RPC_ERROR_BEGIN + 2
RPC_ERROR_UNKNOWN = RPC_ERROR_BEGIN + 3
RPC_ERROR_ENTITY_NOT_FOUND = RPC_ERROR_BEGIN + 4
RPC_ERROR_METHOD_NOT_FOUND = RPC_ERROR_BEGIN + 5
RPC_ERROR_POSITION_CHANGED = RPC_ERROR_BEGIN + 6


class RpcException(Exception):
    def __init__(self, code: int, mas: str):
        self.code = 0
        self.msg = ""

    @staticmethod
    def interface_invalid():
        return RpcException(RPC_ERROR_INTERFACE_INVALID, "interface invalid")

    @staticmethod
    def impl_invalid():
        return RpcException(RPC_ERROR_IMPL_INVALID, "impl invalid")

    @staticmethod
    def entity_not_found():
        return RpcException(RPC_ERROR_ENTITY_NOT_FOUND, "entity not found")

    @staticmethod
    def method_not_found():
        return RpcException(RPC_ERROR_METHOD_NOT_FOUND, "method not found")

    @staticmethod
    def position_changed():
        return RpcException(RPC_ERROR_POSITION_CHANGED, "position changed")


__json_mapper: Dict[str, Any] = dict()


def register_model(cls):
    global __json_mapper
    __json_mapper[cls.__qualname__] = cls


class JsonMeta(type):
    def __new__(cls, class_name, class_parents, class_attr):
        cls = type.__new__(cls, class_name, class_parents, class_attr)
        register_model(cls)
        return cls


def to_dict(obj):
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, "_ast"):
        return to_dict(obj._ast)
    elif hasattr(obj, "__dict__"):
        return {k: to_dict(v) for k, v in obj.__dict__.items() if not callable(v) and not k.startswith('_')}
    elif not isinstance(obj, str) and hasattr(obj, '__iter__'):
        return [to_dict(v) for v in obj]
    else:
        return obj


@dataclass
class JsonMessage(metaclass=JsonMeta):
    @classmethod
    def from_dict(cls, kwargs: dict):
        return cls(**kwargs)

    def to_dict(self) -> dict:
        return cast(dict, to_dict(self))


@dataclass
class RpcMessage:
    meta: JsonMessage
    body: bytes = b''

    @classmethod
    def from_msg(cls, meta: JsonMessage, body: bytes = b'') -> 'RpcMessage':
        msg = RpcMessage(meta=meta, body=body)
        return msg


@dataclass
class RpcRequest(JsonMessage):
    service_name: str = ""
    method_name: str = ""
    actor_id: ActorId = 0
    reentrant_id: int = 0
    request_id: int = 0
    server_id: int = 0
    _args: Optional[list] = None
    _kwargs: Optional[dict] = None

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs


@dataclass
class RpcResponse(JsonMessage):
    request_id: int = 0
    error_code: int = 0
    error_str: str = ""
    _response: Optional[object] = None

    @property
    def response(self):
        return self._response


class SequenceId(object):
    SHIFT = 1000000000

    def __init__(self):
        self._seed = 0
        self._id = 0

    def new_id(self) -> int:
        self._id += 1
        return self._seed

    @property
    def seed(self):
        return self._seed

    def set_seed(self, seed: int):
        if seed <= self._seed:
            raise Exception("seed can not decrease")
        self._seed = seed
        self._id = self._seed * self.SHIFT


_reentrant_id = SequenceId()
_new_request_id = SequenceId()


def new_reentrant_id() -> int:
    return _reentrant_id.new_id()


def new_request_id() -> int:
    return _new_request_id.new_id()


class _RpcMethodObject(object):

    def __init__(self, actor_type: str, actor_id: ActorId, method_name: str, reentrant_id: int):
        self.actor_type = actor_type
        self.actor_id = actor_id
        self.method_name = method_name
        self.reentrant_id = reentrant_id

    async def __send_rpc(self, *args, **kwargs):
        position = await get_placement_impl().find_position(self.actor_type, self.actor_id)
        if position is None:
            raise Exception("Placement Service Invalid")
        session = position.session
        if session is None:
            raise Exception(f"Target Server Invalid, ServerId: {position.server_uid}")

        req = RpcRequest()
        req.request_id = new_request_id()
        req.service_name = self.actor_type
        req.method_name = self.method_name
        req.actor_id = self.actor_id
        req.reentrant_id = self.reentrant_id
        req.server_id = position.server_uid

        raw_args = pickle_dumps((args, kwargs))
        await session.send_message(RpcMessage.from_msg(req, raw_args))
        return req.reentrant_id

    async def __call__(self, *args, **kwargs):
        for x in range(2):
            try:
                request_id = await self.__send_rpc(*args, **kwargs)
                return await _rpc_call(request_id)
            except RpcException as e:
                if e.code == RPC_ERROR_POSITION_CHANGED:
                    get_placement_impl().remove_position_cache(self.actor_type, self.actor_id)
                    continue
                raise e


DEFAULT_RPC_TIMEOUT = 5.0
__future_dict = weakref.WeakKeyDictionary()


def add_future(unique_id: int, future: Future):
    __future_dict[unique_id] = future


async def _rpc_call(unique_id: int) -> object:
    future = asyncio.get_event_loop().create_future()
    add_future(unique_id, future)
    await asyncio.wait_for(future, timeout=DEFAULT_RPC_TIMEOUT)
    ret = future.result()
    return ret


THRESHOLD = 300
COMPRESSED = b'1'
UNCOMPRESSED = b'0'


def pickle_dumps(o: Any) -> bytes:
    array = pickle.dumps(o, protocol=pickle.HIGHEST_PROTOCOL)
    compressed = UNCOMPRESSED + array
    if len(array) > THRESHOLD:
        compressed = lz4.frame.compress(array)
        if len(compressed) < len(array):
            compressed = COMPRESSED + compressed
    return compressed


class _RpcProxyObject(object):

    def __init__(self, s_type: Type, uid: ActorId, context: Optional[ActorContext]):
        self.service_name = s_type.__qualname__
        self.uid = uid
        self.context = None
        if context is not None:
            self.context = weakref.ref(context)

    def __getattr__(self, name: str):
        ctx: Optional[ActorContext] = None
        if self.context is not None:
            ctx = self.context()
        if ctx is not None:
            reentrant_id = ctx.reentrant_id
        else:
            reentrant_id = new_reentrant_id()
        method = _RpcMethodObject(self.service_name, self.uid, name, reentrant_id)
        return method


def get_proxy(s_type: Type[ActorInterfaceType], uid: ActorId, context: ActorContext=None) -> ActorInterfaceType:
    p = _RpcProxyObject(s_type, uid, context)
    return cast(ActorInterfaceType, p)
