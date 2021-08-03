import asyncio
from aiohttp import ClientSession

url = "https://www.baidu.com"


async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.read()
            print(resp)


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello(url))


if __name__ == '__main__':
    run()

#  output:
#  b'<html>\r\n<head>\r\n\t<script>\r\n\t\tlocation.replace(location.href.replace("https://","http://"));\r\n\t</script>\r\n</head>\r\n<body>\r\n\t<noscript><meta http-equiv="refresh" content="0;url=http://www.baidu.com/"></noscript>\r\n</body>\r\n</html>'
