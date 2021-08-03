

def test(name):
    print("starting ... ")

    while True:
        x = yield name
        if not x:
            return "stop"
        print("send ->", x)


def run():
    coro = test("ribincao")
    next(coro)
    print("ret of send ->", coro.send(123))
    print("ret of send ->", coro.send(456))
    try:
        coro.send(None)
    except StopIteration as e:
        print("error: ", e.value)


def for_test():
    for i in range(3):
        yield i


#  打开双向通道，把最外层的调用方和最内层的子生成器连接起来
def yield_from_test():
    yield from range(3)


def for_test_run():
    print(list(for_test()))
    print(list(yield_from_test()))


if __name__ == '__main__':
    nums = yield_from_test()
    for num in nums:
        print(num)
