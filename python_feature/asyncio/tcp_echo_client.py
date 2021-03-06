import asyncio


async def tcp_echo_client(msg: str):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    print(f"Send: {msg!r}")
    writer.write(msg.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f"Received: {data.decode()!r}")

    print("Close the connection")
    writer.close()
    await writer.wait_closed()


if __name__ == '__main__':
    asyncio.run(tcp_echo_client("hello world"))
