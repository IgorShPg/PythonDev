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























with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as COWsocket:
    COWsocket.connect(("localhost", 1337))
    cmdline = COW()
    receiver = threading.Thread(target=receive, args=(cmdline,))
    receiver.start()
    cmdline.cmdloop()