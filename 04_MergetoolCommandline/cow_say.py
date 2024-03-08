import cowsay
import shlex
import cmd
import readline

from default import *

COWSAY_DEFAULTS = COWTHINK_DEFAULTS = {"-e": (cowsay.Option.eyes, str), "-c": ("default", str), "-T": (cowsay.Option.tongue, str)}
MAKE_BUBBLE_DEFAULTS = {"-b": ("cowsay", str), "-d": (40, int), "-w": (True, bool)}
COWSAY_COMPLETE = COWTHINK_COMPLETE = {"-e": ["oo", "XX", "$$", "@@", "**"],"-c": cowsay.list_cows(), "-T": ["  ", "U ", " U", "u ", " u", "||"]}
MAKE_BUBBLE_COMPLETE = {"-b": ["cowsay", "cowthink"], "-d": [], "-w": ["True", "False"]}
COMPLETE = {"cowsay": COWSAY_COMPLETE, "cowthink": COWTHINK_COMPLETE, "make_bubble": MAKE_BUBBLE_COMPLETE}

def parse(args):
    return shlex.split(args)

def get_opt_arg(args, default_values):
    i = 0
    znach = {key: val[0] for key, val in default_values.items()}
    while i < len(args):
        znach[args[i]] = default_values[args[i]][1](args[i + 1])
        i += 2
    return znach


def complete(text, line, begidx, endidx):
    if begidx == endidx :
        key, command = shlex.split(line)[-1] 
    else:
        key, command = shlex.split(line)[-2], shlex.split(line)[0]
    return [s for s in COMPLETE[command][key] if s.startswith(text)]


class COWS(cmd.Cmd):
    prompt = "(COW)"

    def do_list_cows(self, args):
        """
        Печатает всех имеющихся коров.
        
        """
        print(cowsay.list_cows())

    def do_make_bubble(self, args):
        """
        Оборачивает введенный текст в пузырь.
        make_bubble text [-b cowsay | cowthink] [-d width] [-w wrap_text]

        Параметры:
            text    :  выводимое коровой сообщение;
            -b      :  cowsay или cowthink
            -d      :  width
            -w      :  wrap_text
        """
        message, *znach = parse(args)
        znach = get_opt_arg(znach, MAKE_BUBBLE_DEFAULTS)
        print(cowsay.make_bubble(message, brackets=cowsay.THOUGHT_OPTIONS[znach["-b"]], width=znach["-d"],wrap_text=znach["-w"]))

    def complete_make_bubble(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_cowsay(self, args):
        """
        Заставляет корову разговаривать.
        cowsay message [-c cow] [-e eye_string] [-T tongue_string]

        Параметры:
            message :  выводимое коровой сообщение;
            -c      :  имя коровы (смотри list_cows);
            -e      :  строка - глаза коровы;
            -T      :  строка - язык коровы;
        """
        message, *znach = parse(args)
        znach = get_opt_arg(znach, COWSAY_DEFAULTS)
        print(cowsay.cowsay(message, cow=znach["-c"], eyes=znach["-e"], tongue=znach["-T"]))

    def complete_cowsay(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_cowthink(self, args):
        """Команда аналогична cowsay"""
        self.do_cowsay(args)

    def complete_cowthink(self, text, line, begidx, endidx):
        return complete(text, line, begidx, endidx)

    def do_exit(self, args):
        """Выйти из Cow"""
        return True

    def precmd(self, line):
        if line == 'EOF':
            return 'exit'
        return line

    def emptyline(self):
        pass


if __name__ == "__main__":
    COWS().cmdloop()