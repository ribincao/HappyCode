import asyncio
import websockets

async def producer_handler(ws, path):
    print('---- ws 建立链接 ----')
    while True:
        message = input('Please input: ')
        await ws.send(message)

start_server = websockets.serve(producer_handler, 'localhost', 1060)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
