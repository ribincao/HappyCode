import websockets
import asyncio
from services.game import *


async def echo(ws):
    while True:
        async for req in ws:
            await ws.send(req)


async def main(ws, path):
    log.info("client connect")
    while True:
        select = await ws.recv()
        if select == "1" or select == "0":
            break
    try:
        app = Game()
        if select == "1":
            ret = await app.log_in(ws)
            if ret:
                print("log in success")
                log.info("log in success")
                await echo(ws)
        if select == "0":
            ret = await app.sign_up(ws)
            if ret:
                print("sign up success")
                log.info(f"{app.user_name} sign up success")
                await echo(ws)
    except websockets.ConnectionClosedOK:
        print("client closed")
        log.err("client closed")
    except Exception as e:
        print(e)
        log.err(str(e))


if __name__ == '__main__':
    start_server = websockets.serve(main, 'localhost', 1060, ping_interval=200)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
