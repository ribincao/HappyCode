import asyncio
from threading import Thread
from collections import  deque
import random
import time


dq = deque()
# queue = asyncio.Queue()
loop = asyncio.new_event_loop()


def loop_thread():
    asyncio.set_event_loop(loop)
    loop.run_forever()


def consumer_thread():
    while True:
        if dq:
            msg = dq.pop()
            if msg:
                asyncio.run_coroutine_threadsafe(worker(f"test - {msg}"), loop)


async def worker(name):
    print("running ", name)
    return "ret " + name


def main():
    loop_t = Thread(target=loop_thread)
    loop_t.setDaemon(True)
    loop_t.start()

    consumer_t = Thread(target=consumer_thread)
    consumer_t.setDaemon(True)
    consumer_t.start()

    while True:
        i = random.randint(1, 10)
        dq.appendleft(str(i))
        time.sleep(2)


if __name__ == '__main__':
    main()