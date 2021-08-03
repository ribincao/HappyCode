import time
import asyncio

async def hello():
    asyncio.sleep(1)
    print(f"Hello world: {time.time()}")

def run():
    loop = asyncio.get_event_loop()
    for i in range(5):
        loop.run_until_complete(hello())


if __name__ == '__main__':
    run()
