from cowsay import cowsay, list_cows
import argparse
import sys





parser=argparse.ArgumentParser(prog="cowsay", description="Cowsay prog")
parser.add_argument('message',nargs='?',default='',help='cow message')

args=parser.parse_args()

print(cowsay(message=args.message))



