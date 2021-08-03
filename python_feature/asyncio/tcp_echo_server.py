import asyncio
from asyncio import StreamWriter, StreamReader


async def handle_echo(reader: StreamReader, writer: StreamWriter):
    data = await reader.read()
    msg = data.decode()
    address = writer.get_extra_info('peername')

    print(f"Received {msg!r} from {address!r}")

    print(f"Send {msg!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    srv = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    address = srv.sockets[0].getsockname()
    print(f"Serving on {address}")

    async with srv:
        await srv.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
