import time
import asyncio
from aiohttp import ClientSession


tasks = []
url = "https://www.baidu.com/{}"


async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            # print(f"Hello world: {time.time()}")
            return await response.read()


def run():
    loop = asyncio.get_event_loop()
    for i in range(5):
        task = asyncio.ensure_future(hello(url.format(i)))
        tasks.append(task)
    ret = loop.run_until_complete(asyncio.gather(*tasks))
    for resp in ret:
        print(resp)



if __name__ == '__main__':
    run()
