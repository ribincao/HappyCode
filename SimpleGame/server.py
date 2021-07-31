import websockets
import asyncio
from util.redisManager import r
from util.logManager import log


async def login_game(ws):
    cnt = 2
    while True:
        if cnt <= 0:
            return False

        req = await ws.recv()
        req = req.split(":")
        if len(req) != 2:
            rsp = f"wrong input, please retry(username:passwd), {cnt} times left"
            await ws.send(rsp)
            cnt -= 1
            log.err(rsp)
            continue

        name, passwd = req[0], req[1]
        if not r.get(name + ":username"):
            rsp = f"there is no {name} in server, please retry, {cnt} times left"
            await ws.send(rsp)
            cnt -= 1
            log.err(rsp)
            continue

        if r.get(name + ":passwd") == passwd:
            rsp = f"welcome {name}"
            await ws.send(rsp)
            log.info(rsp)
            return True

        rsp = f" {passwd} is wrong, please retry, {cnt} times left"
        await ws.send(rsp)
        cnt -= 1
        log.err(rsp)


async def echo(ws):
    while True:
        async for req in ws:
            await ws.send(req)


async def main(ws, path):
    print("[INFO] client connect")
    log.info("client connect")
    try:
        ret = await login_game(ws)
        if ret:
            print("log in success")
            log.info("log in success")
            await echo(ws)
    except websockets.ConnectionClosedOK:
        print("client closed")
        log.err("client closed")
    except Exception as e:
        print(e)
        log.err(str(e))


if __name__ == '__main__':
    start_server = websockets.serve(main, 'localhost', 1060)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()