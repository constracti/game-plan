import copy
import itertools
import math
import time

def game_rules_check(table, r, g, th, ta, rules=[]):
	for rule in rules:
		if rule[0] == "consecutive":
			if len(rule) == 2:
				if r > 0:
					g1, g2 = rule[1]
					if g == g1:
						if th in table[r-1][g2] or ta in table[r-1][g2]:
							return False
					elif g == g2:
						if th in table[r-1][g1] or ta in table[r-1][g1]:
							return False
	return True

def game_rules_score(table, rules=[]):
	n = len(table)
	score = None
	for rule in rules:
		if rule[0] == "consecutive":
			if len(rule) > 2:
				if score is None:
					score = 0
				for r in range(n-1):
					g1, g2 = rule[1]
					if table[r][g1][0] in table[r+1][g2] or table[r][g1][1] in table[r+1][g2]:
						score -= 1
					if table[r][g2][0] in table[r+1][g1] or table[r][g2][1] in table[r+1][g1]:
						score -= 1
	return score

def print_table(table, teams=None):
		if teams is not None:
			assert len(teams) == 2 * len(table)
			maxlen = max([len(team) for team in teams])
			for round in table:
				print(" ".join([teams[t].ljust(maxlen) for pair in round for t in pair]))
		else:
			for round in table:
				print("\t".join([str(team) for pair in round for team in pair]))
		print()

def search(n, rules=[], stop=None, echo=False):
	assert n > 0
	searchobj = {
		"n": n,
		"rules": rules,
		"stop": stop,
		"echo": echo,
		"table": [[None] * n for r in range(n)],
		"pairs": [[False] * (2*n) for th in range(2*n)],
		"games": [[False] * (2*n) for g in range(n)],
		"rounds": [[False] * (2*n) for r in range(n)],
		"solutions": [],
	}
	if echo:
		print("teams {}".format(2*n))
		print()
		for rule in rules:
			print(rule)
		print()
	for g in range(n):
		assert searchobj_add_pair(searchobj, 0, g, 2*g, 2*g+1)
	searchobj_dfs(searchobj, 1, 0)
	return searchobj["solutions"]

def searchobj_add_pair(searchobj, r, g, th, ta):
	if searchobj["pairs"][th][ta]:
		return False
	if searchobj["rounds"][r][th] or searchobj["rounds"][r][ta]:
		return False
	if searchobj["games"][g][th] or searchobj["games"][g][ta]:
		return False
	if not game_rules_check(searchobj["table"], r, g, th, ta, rules=searchobj["rules"]):
		return False
	searchobj["table"][r][g] = (th, ta)
	searchobj["pairs"][th][ta] = True
	searchobj["rounds"][r][th] = True
	searchobj["rounds"][r][ta] = True
	searchobj["games"][g][th] = True
	searchobj["games"][g][ta] = True
	return True

def searchobj_del_pair(searchobj, r, g):
	assert searchobj["table"][r][g] is not None
	th, ta = searchobj["table"][r][g]
	searchobj["table"][r][g] = None
	searchobj["pairs"][th][ta] = False
	searchobj["rounds"][r][th] = False
	searchobj["rounds"][r][ta] = False
	searchobj["games"][g][th] = False
	searchobj["games"][g][ta] = False

def searchobj_dfs(searchobj, r, g):
	if r == searchobj["n"]:
		if searchobj["echo"]:
			score = game_rules_score(searchobj["table"], searchobj["rules"])
			if score is None:
				print("table {}".format(len(searchobj["solutions"])))
			else:
				print("table {} - score {}".format(len(searchobj["solutions"]), score))
			print_table(searchobj["table"])
		searchobj["solutions"].append(copy.deepcopy(searchobj["table"]))
		if searchobj["stop"] is not None:
			searchobj["stop"] -= 1
	else:
		for th in range(0, 2*searchobj["n"]-1):
			for ta in range(th+1, 2*searchobj["n"]):
				if searchobj_add_pair(searchobj, r, g, th, ta):
					if g == searchobj["n"]-1:
						searchobj_dfs(searchobj, r+1, 0)
					else:
						searchobj_dfs(searchobj, r, g+1)
					searchobj_del_pair(searchobj, r, g)
					if searchobj["stop"] is not None and not searchobj["stop"]:
						return

def team_rules_score(table, teams, rules=[]):
	score = 0
	for rule in rules:
		if rule[0] == "match":
			g = rule[1]
			t1, t2 = rule[2]
			for round in table:
				if t1 in round[g] and t2 in round[g]:
					score += rule[3]
		elif rule[0] == "level":
			g = rule[1]
			for round in table:
				l1, l2 = [teams[t][1] for t in round[g]]
				if l1 is not None and l2 is not None:
					score += rule[2] * abs(l1 - l2)
		elif rule[0] == "pair":
			t1, t2 = rule[1]
			for round in table:
				for pair in round:
					if t1 in pair and t2 in pair:
						score += rule[2]
	return score

def assign(n, tables, rules=[], stop=None):
	table0 = None
	score0 = None
	iter = 0
	itermax = math.factorial(2*n) * len(tables)
	ts0 = time.time()
	for perm in itertools.permutations(range(2*n)):
		for table in tables:
			table = [[tuple([perm[t] for t in pair]) for pair in round] for round in table]
			score = team_rules_score(table, teams, rules)
			iter += 1
			ts = time.time()
			if ts - ts0 >= 10:
				ts0 = ts
				print("progress: {:0.2f}%".format(100 * iter / itermax))
				print()
			if score0 is None or score0 < score:
				table0 = table
				score0 = score
				print("score: {}".format(score0))
				print_table(table, teams=[team[0] for team in teams])
				if stop is not None and score >= stop:
					return table0
	return table0

n = 5

games = ["Football-old", "Football-new", "Basketball", "Germaniko", "Mila"]
assert len(games) == n
game_rules = [
#	("consecutive", (0, 1), -1),
	("consecutive", (0, 1)),
#	("consecutive", (1, 2)),
#	("consecutive", (2, 0)),
#	("consecutive", (2, 3)),
	("consecutive", (3, 4)),
#	("consecutive", (4, 5)),
]
tables = search(n, rules=game_rules, stop=4)

teams = [
	("AgPar-bg", 5.5),    # 0
	("AgPar-sm", 3.5),    # 1
	("Kallithea", None),  # 2
	("Koropi", None),     # 3
	("Kypseli", None),    # 4
	("Marousi-bg", 6),    # 5
	("Marousi-sm", 4),    # 6
	("Pefki", None),      # 7
	("Peristeri", None),  # 8
	("Xylokastro", None), # 9
]
assert len(teams) == 2 * n
team_rules = [
	("match", 0, (0, 5), +10),
	("match", 1, (0, 5), +8),
	("match", 0, (1, 6), +4),
	("match", 1, (1, 6), +6),
	("level", 0, -2),
	("level", 1, -2),
	("level", 2, -3),
	("level", 3, -1),
	("pair", (0, 1), -10),
	("pair", (5, 6), -10),
]

table = assign(n, tables, team_rules, stop=14)
