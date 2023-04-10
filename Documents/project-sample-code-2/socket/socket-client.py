# more details at: 
#   https://docs.python.org/3/library/asyncio-stream.html#examples

import asyncio, sys

async def tcp_client(message):
    reader, writer = \
        await asyncio.open_connection(
            '127.0.0.1', 5555)

    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'{data.decode()!r}')

    writer.close()

file_name = sys.argv[1]
asyncio.run(tcp_client(file_name))
