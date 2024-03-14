import cowsay
import asyncio
import shlex




clients={}
cows_in_chat = set()

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = [asyncio.Queue(), None]
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me][0].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                match q.result().decode().split(maxsplit=2):
                    case ["who", ]:
                        await clients[me][0].put(f"{[client for client in clients.keys() if client in cowsay.list_cows()]}")
                    case ["cows", ]:
                        await clients[me][0].put(f"{[cow for cow in cowsay.list_cows() if cow not in clients.keys()]}")
                    case ["login", cow]:
                        if cow in cowsay.list_cows():
                            if cow in cows_in_chat:
                                await clients[me][0].put("Cow name is already taken")
                            else:
                                clients[me][1] = cow
                        else:
                            await clients[me][0].put("Unacceptable cow name")
                    case ["say", cow, text]:
                        pass
                    case ["yield", text]:
                        pass
                    case ["quit"]:
                        pass
                # for out in clients.values():
                #     if out is not clients[me]:
                #         await out.put(f"{me} {q.result().decode().strip()}")
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())