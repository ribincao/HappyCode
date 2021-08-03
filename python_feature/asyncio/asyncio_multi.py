import time
import asyncio
from aiohttp import ClientSession


tasks = []
url = "https://www.baidu.com/{}"


async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.read()
            print(f"Hello world: {time.time()} - {resp}")


def run():
    loop = asyncio.get_event_loop()
    for i in range(5):
        task = asyncio.ensure_future(hello(url.format(i)))
        tasks.append(task)
    #  asyncio.wait() 本身是一个协程, 用来包裹多个协程实现多任务控制
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    run()

# output:
# Hello world: 1626847847.656907 - b'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<h1>Not Found</h1>\n<p>The requested URL /1 was not found on this server.</p>\n</body></html>\n'
# Hello world: 1626847847.660896 - b'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<h1>Not Found</h1>\n<p>The requested URL /0 was not found on this server.</p>\n</body></html>\n'
# Hello world: 1626847847.696369 - b'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<h1>Not Found</h1>\n<p>The requested URL /2 was not found on this server.</p>\n</body></html>\n'
# Hello world: 1626847847.713996 - b'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<h1>Not Found</h1>\n<p>The requested URL /4 was not found on this server.</p>\n</body></html>\n'
# Hello world: 1626847847.717985 - b'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<h1>Not Found</h1>\n<p>The requested URL /3 was not found on this server.</p>\n</body></html>\n'
