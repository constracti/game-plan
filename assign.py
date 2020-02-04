import argparse
import itertools
import sys

from common import *
import config


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--infile")
parser.add_argument("-o", "--outfile")
parser.add_argument("--score", default=0., type=float)

args = parser.parse_args()

if args.infile is not None:
	args.infile = open(args.infile, "r")
else:
	args.infile = sys.stdin

if args.outfile is not None:
	args.outfile = open(args.outfile, "w")


sols = file2sols(args.infile, config.games, config.teams)


def assign(games, teams, rules=[], minscore=0.):
	global args
	i = 0
	for perm in itertools.permutations(range(len(teams))):
		if i % 1000 == 0:
			print("# permutation {}".format(i))
		i += 1
		for sol in sols:
			sol = [[tuple(perm[t] for t in ts) for ts in row ] for row in sol]
			score = 0.
			valid = True
			for rule in rules:
				if rule.score is not None:
					score += rule.eval(sol, games, teams)
				elif not rule.test(sol, games, teams):
					valid = False
					break
			if not valid:
				continue
			if score < minscore:
				continue
			print("# success {}".format(i))
			print("# score {}".format(score), file=args.outfile)
			return sol
	print("# failure")
	assert False

sol = assign(config.games, config.teams, config.trules, args.score)

for row in sol:
	line = row2line(row)
	print("\t".join(str(t) for t in line), file=args.outfile)
