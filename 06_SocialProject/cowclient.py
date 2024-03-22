import shlex
import cmd
import socket
import readline
import threading
from copy import copy


receiving = True
completion = None



def parse(args):
    return shlex.split(args)



def complete(text, line, req):
    global completion
    if text and len(shlex.split(line)) == 2 or not text and len(shlex.split(line)) == 1:
        request(f"{req} {text if text else ''}")

    while completion is None:
        continue
    comp = copy(completion)
    completion = None

    return comp


def receive(cmdline):
    global receiving, COWsocket, completion
    while receiving:
        msg = COWsocket.recv(1024).decode()
        if msg.strip() == "exit":
            break
        elif msg.startswith("["):
            completion = eval(msg)
        else:
            print(f"\n{msg.strip()}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)

def request(req):
    global COWsocket
    COWsocket.send(f"{req}\n".encode())




class COW(cmd.Cmd):
    intro = "<<<Welcome to cowchat>>>"
    prompt = "(COW_CHAT)"

    def do_login(self, args):
        match parse(args):
            case [name, ]:
                request(f"login {name}")
            case _:
                print("There should be one argument")

    
    def complete_login(self, text, line, begidx, endidx):
        return complete(text, line, "complete_login")

    def do_who(self, args):
        request("who")

    def do_cows(self, args):
        request("cows")

    def do_say(self, args):
        match parse(args):
            case [cow, text, ]:
                request(f"say {cow} {text}")
            case _:
                print("There should be two arguments")

    def complete_say(self, text, line, begidx, endidx):
        return complete(text, line, "complete_say")

    def do_yield(self, args):
        match parse(args):
            case [text, ]:
                request(f"yield {text}")
            case _:
                print("There should be one argument")

    def do_quit(self, args):
        global receiving
        request("quit")
        receiving = False
        return True





with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as COWsocket:
    COWsocket.connect(("localhost", 1337))
    cmdline = COW()
    receiver = threading.Thread(target=receive, args=(cmdline,))
    receiver.start()
    cmdline.cmdloop()