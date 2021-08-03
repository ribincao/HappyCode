import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://localhost:8765') as websock:
        name = input('Your name: ')
        await websock.send(name)
        print(name)
        greeting = await websock.recv()
        print(greeting)

asyncio.get_event_loop().run_until_complete(hello())
