class Game:

	def __init__(self, name, cat=None, teams=2):
		self.name = name
		self.cat = cat
		self.teams = teams


class GameRule:

	def __init__(self, name):
		self.name = name

	def search_apply(self, so, r, g, ts):
		if self.name == "consecutive":
			if r == 0:
				return True
			cat = so.games[g].cat
			if cat is None:
				return True
			for g0, game in enumerate(so.games):
				if game.cat != cat:
					continue
				if set(so.table[r-1][g0]) & set(ts):
					return False
			return True
		else:
			return True


class Team:

	def __init__(self, name, level=None):
		self.name = name
		self.level = level


class TeamRule:

	def eval(self, sol, games, teams):
		assert False

	def test(self, sol, games, teams):
		assert False


class PairTeamRule(TeamRule):

	def __init__(self, pair, cat=None, score=None):
		self.name = "pair"
		self.pair = pair
		self.cat = cat
		self.score = score

	def eval(self, sol, games, teams):
		assert self.score is not None
		score = 0.
		for row in sol:
			for game, ts in zip(games, row):
				if self.cat is not None and game.cat != self.cat:
					continue
				names = [teams[t].name for t in ts]
				if not all(name in names for name in self.pair):
					continue
				score += self.score
		return score

	def test(self, sol, games, teams):
		assert self.score is None
		for row in sol:
			for game, ts in zip(game, row):
				if self.cat is not None and game.cat != self.cat:
					continue
				names = [teams[t].name for t in ts]
				if not all(name in names for name in self.pair):
					continue
				return False
		return True


class LevelTeamRule(TeamRule):

	def __init__(self, cat, score):
		assert cat is not None
		assert score is not None
		self.name = "level"
		self.cat = cat
		self.score = score

	def eval(self, sol, games, teams):
		score = 0.
		for row in sol:
			for game, ts in zip(games, row):
				if game.cat != self.cat:
					continue
				levels = [teams[t].level for t in ts]
				levels = [l for l in levels if l is not None]
				if not levels:
					continue
				score += self.score * (max(levels) - min(levels))
		return score


def row2line(row):
	line = []
	for ts in row:
		if ts is not None:
			line.extend(ts)
	return line


def line2row(line, games):
	row = []
	t0 = 0
	for game in games:
		t1 = t0 + game.teams
		ts = tuple(line[t0:t1])
		t0 = t1
		row.append(ts)
	return row

def file2sols(infile, games, teams):
	glen = len(games)
	tlen = len(teams)
	sols = []
	sol = []
	while True:
		line = infile.readline()
		if line == "":
			assert not sol
			return sols
		line = line.rstrip()
		if line == "" or line.startswith("#"):
			continue
		line = line.split("\t")
		assert len(line) == tlen
		line = [int(t) for t in line]
		row = line2row(line, games)
		sol.append(row)
		if len(sol) == glen:
			sols.append(sol)
			sol = []
