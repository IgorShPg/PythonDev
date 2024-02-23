from cowsay import cowsay, list_cows
import argparse


def parseArgs(parser):

    parser.add_argument('message', nargs='?', default='', help='cow message')
    parser.add_argument('-e', default='oo')
    parser.add_argument('-l', action='store_true')
    parser.add_argument("-f")
    parser.add_argument("-n", action="store_false")
    parser.add_argument('-T', default='')
    parser.add_argument("-W", default=40, type=int)
    parser.add_argument('-b', action='store_true')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('-g', action='store_true')
    parser.add_argument('-p', action='store_true')
    parser.add_argument('-s', action='store_true')
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-w', action='store_true')
    parser.add_argument('-y', action='store_true')

    args = parser.parse_args()
    preset = ''.join([i for i in "bdgpstwy" if i in args.__dict__])
    return args, preset



parser = argparse.ArgumentParser(prog="cowsay", description="Cowsay program")
args, preset = parseArgs(parser)

if args.l:
    print(list_cows())
else:
    print(cowsay(args.message, preset=preset, eyes=args.e, tongue=args.T,width=args.W, wrap_text=args.n, cowfile=args.f))





