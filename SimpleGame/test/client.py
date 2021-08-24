import asyncio
import websockets


async def test():
    async with websockets.connect('ws://localhost:1061/hello') as ws:
        while True:
            select = input("say: ")
            try:
                await ws.send(select)
            except websockets.ConnectionClosedOK:
                print("connect closed.")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
