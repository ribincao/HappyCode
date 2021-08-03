import asyncio
from threading import Thread


#  创建一个线程让事件循环在线程内永久运行
def main_thread(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def example(name):
    print("call back name: ", name)
    return "ret: " + name


def main():
    loop = asyncio.new_event_loop()
    t = Thread(target=main_thread, args=(loop, ))
    t.start()

    handle = loop.call_soon_threadsafe(example, "1")
    print(handle)
    handle.cancel()

    #  call_soon_threadsafe
    loop.call_soon_threadsafe(example, "2")
    print("continue...")

    loop.call_soon_threadsafe(example, "3")
    print("hi...")


async def coro_example(name):
    print("runing -> ", name)
    await asyncio.sleep(1)
    return "ret " + name


def run():
    loop = asyncio.new_event_loop()
    t = Thread(target=main_thread, args=(loop, ))
    t.start()

    future = asyncio.run_coroutine_threadsafe(coro_example("1"), loop)
    print(future.result())
    asyncio.run_coroutine_threadsafe(coro_example("2"), loop)
    print("continue")
    asyncio.run_coroutine_threadsafe(coro_example("3"), loop)
    print("hi")


if __name__ == '__main__':
    run()
