from ..util.redisManager import r
from ..util.logManager import log


class Game:

    def __init__(self):
        self.log_in_times_limit = 2
        self.user_name = ""

    async def sign_up(self, ws):
        while True:
            req = await ws.recv()
            req = req.split(":")
            name, passwd = req[0], req[1]
            if r.get(name + ":user_name"):
                rsp = f"{name} existed."
                await ws.send(rsp)
                continue
            r.set(name + ":user_name", name)
            r.set(name + ":passwd", passwd)
            self.user_name = name
            await ws.send("Sign up Success")
            return True

    async def log_in(self, ws):
        cnt = self.log_in_times_limit
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
            if not r.get(name + ":user_name"):
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

            rsp = f"passwd is wrong, please retry, {cnt} times left"
            await ws.send(rsp)
            cnt -= 1
            log.err(rsp)
