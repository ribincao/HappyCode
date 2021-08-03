import asyncio


async def waiter(event: asyncio.Event):
    print("waiting...")
    await event.wait()
    print("got it!")


async def run():
    event = asyncio.Event()

    waiter_task = asyncio.create_task(waiter(event))

    await asyncio.sleep(1)
    event.set()

    await waiter_task


if __name__ == '__main__':
    asyncio.run(run())
