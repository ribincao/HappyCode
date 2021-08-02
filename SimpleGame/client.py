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


async def sign_up(ws):
    while True:
        username = input("Please Input your username:\n")
        passwd = input("Please input your password:\n")
        req = username + ":" + passwd
        try:
            await ws.send(req)
            rsp = await ws.recv()
        except websockets.ConnectionClosedError:
            print("server closed")
            return False
        if "Success" in rsp:
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
        select = ''
        while select != "0" and select != "1":
            select = input("Please select([1] -- sign in | [0] -- sign up):\n")
        try:
            await ws.send(select)
            if select == '1':
                ret = await auth(ws)
                if ret:
                    print("log in success")
                    await talk(ws)
            if select == '0':
                ret = await sign_up(ws)
                if ret:
                    print("sign up success.")
                    await talk(ws)
        except websockets.ConnectionClosedOK:
            print("connect closed.")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
