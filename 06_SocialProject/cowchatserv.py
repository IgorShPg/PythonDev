import asyncio
import cowsay
import shlex

clients = {}
cows_in_chat = {}
cows_chatting = {}


def who(who_prefix=None):
    who = list(cows_in_chat.keys())
    if who_prefix is not None:
        who = f"{[w for w in who if w.startswith(who_prefix)]}"
    else:
        who = f" {who}"

    return who

def cows(cow_prefix=None):
    cows = [cow for cow in cowsay.list_cows() if cow not in cows_in_chat]
    if cow_prefix is not None:
        cows = f"{[cow for cow in cows if cow.startswith(cow_prefix)]}"
    else:
        cows = f" {cows}"

    return cows

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    my_name=""
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                command=shlex.split(q.result().decode())
                match command:
                    case ["who", ]:
                        await clients[me].put(who())
                    case ["cows", ]:
                        await clients[me].put(cows())
                    case ["login", cow]:
                        if cow in cowsay.list_cows():
                            if cow in cows_in_chat:
                                await clients[me].put("Cow name is already taken")
                            else:
                                cows_in_chat[cow] = clients[me]
                                cows_chatting[clients[me]] = cow
                                my_name=cow
                        else:
                            await clients[me].put("Unacceptable cow name")
                    case ["complete_login", prefix]:
                        await clients[me].put(cows(prefix))
                    case ["say", cow, *message]:
                        if my_name!="":
                            if cow in cows_in_chat:
                                await cows_in_chat[cow].put("" + cowsay.cowsay("".join(message), cow=cows_chatting[clients[me]]))
                            else:
                                await clients[me].put("There is no cow with such name")
                        else:
                           await clients[me].put("Before chatting you must log in") 
                    case ["complete_say", prefix]:
                        await clients[me].put(who(prefix))
                    case ["yield", *message]:
                        if my_name!="":
                            for cow in cows_in_chat:
                                if cows_in_chat[cow] != clients[me]:
                                    await cows_in_chat[cow].put("" + cowsay.cowsay("".join(message), cow=cows_chatting[clients[me]]))
                        else:
                           await clients[me].put("Before chatting you must log in") 
                    case ["quit"]:
                        cow = cows_chatting[clients[me]]
                        cows_in_chat.pop(cow)
                        cows_chatting.pop(clients[me])
                        send.cancel()
                        receive.cancel()
                        print(me, "DONE")
                        del clients[me]
                        writer.close()
                        await writer.wait_closed()

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