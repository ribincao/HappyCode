import asyncio


async def hello():
    await asyncio.sleep(1)
    return "Hello World"


def get_coro_result_1():
    coro = hello()
    loop = asyncio.get_event_loop()
    task = loop.create_task(coro)
    try:
        print("ret ->", task.result())
    except asyncio.InvalidStateError as e:
        print("error")

    loop.run_until_complete(task)
    print("ret again -> ", task.result())
    loop.close()


def call_back(future: asyncio.Future):
    print("ret -> ", future.result())


def get_coro_result_2():
    coro = hello()
    loop = asyncio.get_event_loop()
    task = loop.create_task(coro)
    task.add_done_callback(call_back)
    loop.run_until_complete(task)
    loop.close()


if __name__ == '__main__':
    #  通过 task.result() 获取协程返回值, 不过需要 task 完成, 否则返回 InvalidStateError 错误
    get_coro_result_1()
    #  通过 task.add_done_callback 添加回调获取协程返回值
    get_coro_result_2()

    # ret = loop.run_until_complete(asyncio.gather(*tasks))
