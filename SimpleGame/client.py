import asyncio
import websockets


async def auth(ws):
    while True:
        req = input("log in (username:passwd): ")
        try:
            await ws.send(req)
            rsp = await ws.recv()
        except websockets.ConnectionClosedError:
            print("server closed")
            return False
        if "welcome" in rsp:
            return True
        print(rsp)


async def talk(ws):
    while True:
        data = input("say something: \n")
        await ws.send(data)
        rsp = await ws.recv()
        print(rsp)


async def main():
    async with websockets.connect('ws://localhost:1060') as ws:
        try:
            ret = await auth(ws)
            if ret:
                print("log in success")
                await talk(ws)
        except websockets.ConnectionClosedOK:
            print("connect closed.")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
