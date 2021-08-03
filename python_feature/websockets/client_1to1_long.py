import asyncio
import websockets

async def consumer_handler():
    async with websockets.connect('ws://localhost:1060') as websock:
        async for message in websock:
            print(message)

asyncio.get_event_loop().run_until_complete(consumer_handler())
