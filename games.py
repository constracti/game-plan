import argparse
import sys

from common import *
import config


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--infile")
parser.add_argument("-o", "--outfile")
parser.add_argument("-s", "--separator", default="tab", choices=["tab", "comma", "semicolon"])

args = parser.parse_args()

if args.infile is not None:
	args.infile = open(args.infile, "r")
else:
	args.infile = sys.stdin

if args.outfile is not None:
	args.outfile = open(args.outfile, "w")

if args.separator == "comma":
	args.separator = ","
elif args.separator == "semicolon":
	args.separator = ";"
else:
	args.separator = "\t"
	

sol = file2sols(args.infile, config.games, config.teams)
assert len(sol) == 1
sol = sol[0]


for game in config.games:
	print(game.name + args.separator * game.teams, end="", file=args.outfile)
print(file=args.outfile)

for row in sol:
	for ts in row:
		for t in ts:
			print(config.teams[t].name, end=args.separator, file=args.outfile)
	print(file=args.outfile)
