import asyncio


async def handle(reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
    print("Client:", writer.get_extra_info("peername"))
    while not reader.at_eof():
        msg = await reader.read(128)
        writer.write(msg)
        await writer.drain()
    print("Client:", writer.get_extra_info("peername"), "Disconnected")


async def main(ip4="127.0.0.1",
               port=10000):
    srv = await asyncio.start_server(handle, ip4, port)
    print("Server:", srv.sockets[0].getsockname())
    return await srv.serve_forever()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=10000)

    args = parser.parse_args()
    asyncio.run(main(**args.__dict__))
