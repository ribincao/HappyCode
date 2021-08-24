from typing import *


# alias
Vector = List[float]
Options = Dict[str, str]
Address = Tuple[str, int]
Port = Union[str, int]
Host = Optional[int]  # Union[int, None
# Mode = Literal['r', 'w', 'rb', 'wb']
# Const: Final = 3.14

# new type: int <- UserId <- PlayId
UserId = NewType("UserId", int)
PlayId = NewType("PlayId", UserId)

# Callable: [[argType, argType], returnType]
fun = Callable[[int, int], int]

# Iterable
nums = Iterable[int]

# Container
plays = Sequence[int]
users = Mapping[int, str]

# Generic
T = TypeVar('T')  # Can be anything
S = TypeVar('S', int, str)  # Must be str or int


class Test(Generic[T, S]):
    def __init__(self, name: T):
        self.name = name


def f(t: Test[int, str]):
    print(t.name)


if __name__ == '__main__':
    a: Test[str, str] = Test("a")
    f(a)
    b = cast(Test[int, str], a)
    f(b)

    A = Type
    def f(a: A):
        print(a)
        pass
    f(type(1))

