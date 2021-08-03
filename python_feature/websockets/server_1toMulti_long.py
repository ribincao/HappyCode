import asyncio
import logging
import websockets

logging.basicConfig()

Users = set()

async def notify_users():
    if Users:
        message = input('Please input: ')
        await asyncio.wait([user.send(message) for user in Users])

async def register(ws):
    Users.add(ws)
    await notify_users()

async def unregister(ws):
    Users.remove(ws)
    await notify_users

async def counter(ws, path):
    await register(ws)
    try:
        async for message in ws:
            print(message)
    finally:
        await unregister(ws)

start_server = websockets.serve(counter, 'localhost', 1060)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
