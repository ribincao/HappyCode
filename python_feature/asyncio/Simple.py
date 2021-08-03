import time
import asyncio


# 通过装饰器使得旧式的基于生成器的协程能与 async/await 代码相兼容
@asyncio.coroutine
def old_sleep():
    yield from asyncio.sleep(1)


async def new_sleep():
    await old_sleep()


# async def 定义一个协程函数
async def say(delay, msg):
    #  2. await
    await asyncio.sleep(delay)
    print(msg)


async def main():
    # 3. create_task 把协程封装成一个task
    task1 = asyncio.create_task(say(1, 'hello'))
    task2 = asyncio.create_task(say(2, 'world'))

    print(f"start at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")

if __name__ == '__main__':
    main()  # 简单的调用一个协程并不会使其被调度执行
    asyncio.run(main())  # 1. run
