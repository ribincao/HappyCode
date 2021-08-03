import websockets
import asyncio

async def hello(websocket, path):
    # while True:
    print('---- hello opened ----')
    name = await websocket.recv()
    print(name)
    greeting = f'hello {name}'
    await websocket.send(greeting)
    print(greeting)
    
start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()