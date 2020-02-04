import argparse
import copy
import itertools

from common import *
import config


class SearchObj:

	def __init__(self, games):
		self.games = games
		self.glen = len(games)
		self.tlen = sum(game.teams for game in games)
		self.table = [[None] * self.glen for _ in range(self.glen)]
		self.pairs = [[False] * self.tlen for _ in range(self.tlen)]
		self.tgames = [[False] * self.tlen for _ in range(self.glen)]
		self.trounds = [[False] * self.tlen for _ in range(self.glen)]

	def search(self, rules=[], stop=1):
		self.rules = rules
		self.stop = stop
		self.sols = []
		t = 0
		for g, game in enumerate(self.games):
			ts = tuple(range(t, t + game.teams))
			t += game.teams
			assert self.add_match(0, g, ts)
		assert t == self.tlen
		self._dfs(1, 0)
		for g in reversed(range(self.glen)):
			self.del_match(0, g)

	def _dfs(self, r, g):
		if r < self.glen:
			for ts in itertools.combinations(range(self.tlen), self.games[g].teams):
				if self.add_match(r, g, ts):
					if g == self.glen - 1:
						self._dfs(r+1, 0)
					else:
						self._dfs(r, g+1)
					self.del_match(r, g)
					if self.stop > 0 and self.stop <= len(self.sols):
						return
		else:
			self.print_sol()
			self.sols.append(copy.deepcopy(self.table))

	def add_match(self, r, g, ts):
		assert self.table[r][g] is None
		assert self.games[g].teams == len(ts)
		if any(self.tgames[g][t] for t in ts):
			return False
		if any(self.trounds[r][t] for t in ts):
			return False
		pairs = list(itertools.combinations(ts, 2))
		if any(self.pairs[th][ta] for th, ta in pairs):
			return False
		if any(not rule.search_apply(so, r, g, ts) for rule in self.rules):
			return False
		self.table[r][g] = ts
		for th, ta in pairs:
			self.pairs[th][ta] = True
		for t in ts:
			self.tgames[g][t] = True
		for t in ts:
			self.trounds[r][t] = True
		return True

	def del_match(self, r, g):
		ts = self.table[r][g]
		assert ts is not None
		assert all(self.tgames[g][t] for t in ts)
		assert all(self.trounds[r][t] for t in ts)
		pairs = list(itertools.combinations(ts, 2))
		assert all(self.pairs[th][ta] for th, ta in pairs)
		self.table[r][g] = None
		for th, ta in pairs:
			self.pairs[th][ta] = False
		for t in ts:
			self.tgames[g][t] = False
		for t in ts:
			self.trounds[r][t] = False

	def print_sol(self, sol=None):
		global args
		if sol is None:
			sol = self.table
		for row in sol:
			line = row2line(row)
			print("\t".join(str(t) for t in line), file=args.outfile)
		print(file=args.outfile)

	def print_sols(self):
		global args
		for i, sol in enumerate(self.sols):
			print("# solution {}".format(i), file=args.outfile)
			self.print_sol(sol)


parser = argparse.ArgumentParser()
parser.add_argument("--stop", default=1, type=int)
parser.add_argument("-o", "--outfile")

args = parser.parse_args()
assert args.stop >= 0
if args.outfile is not None:
	args.outfile = open(args.outfile, "w")

so = SearchObj(config.games)
so.search(config.grules, stop=args.stop)
#so.print_sols()
