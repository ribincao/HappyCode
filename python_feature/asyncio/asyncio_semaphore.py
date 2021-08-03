import time
import asyncio
from aiohttp import ClientSession


tasks = []
url = "https://www.baidu.com"


async def hello(url, semaphore):
    async with semaphore:
        async with ClientSession() as session:
            async with session.get(url) as response:
                print(f"Hello world: {time.time()}")
                return await response.read()


async def run():
    semaphore = asyncio.Semaphore(100)
    ret = [hello(url, semaphore) for _ in range(200)]
    print(len(ret))
    await asyncio.wait(ret)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()


if __name__ == '__main__':
    main()
