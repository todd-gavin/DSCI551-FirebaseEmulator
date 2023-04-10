# more details at: 
#   https://docs.python.org/3/library/asyncio-stream.html#examples

import asyncio

async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()

    if (message == 'file1'):
    	writer.write(b'1KB')
    else:
    	writer.write(b'File not found!')

    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 5555)

    async with server:
        await server.serve_forever()

asyncio.run(main())
