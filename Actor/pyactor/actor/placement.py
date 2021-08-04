from typing import Optional
from abc import ABC
from node import *


class Placement(ABC):

    def __init__(self):
        pass

    async def find_position(self, s_type: str, uid: int) -> Optional[ServeNode]:
        pass

    def remove_position_cache(self, s_type: str, uid: int):
        pass


__placement_impl: Optional[Placement] = None


def get_placement_impl() -> Placement:
    assert __placement_impl
    return __placement_impl
