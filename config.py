from common import *


games = [
	Game("Π. Ποδόσφαιρο", cat="football"),
	Game("Κ. Ποδόσφαιρο", cat="football"),
	Game("Μπάσκετ", cat="basketball"),
	Game("Γερμανικό", cat="germaniko"),
	Game("Μήλα"),
]


grules = [
	GameRule("consecutive"),
]


teams = [
	Team("Αγία Παρασκευή - μεγάλο", level=5.5),
	Team("Αγία Παρασκευή - μικρό", level=3.5),
	Team("Καλλιθέα"),
	Team("Κορωπί"),
	Team("Κυψέλη"),
	Team("Μαρούσι - μεγάλο", level=5.5),
	Team("Μαρούσι - μικρό", level=3.5),
	Team("Ξυλόκαστρο"),
	Team("Πεύκη"),
	Team("Περιστέρι"),
]

assert len(teams) == sum(game.teams for game in games)

trules = [
	PairTeamRule(("Αγία Παρασκευή - μεγάλο", "Αγία Παρασκευή - μικρό"), None, -20),
	PairTeamRule(("Μαρούσι - μεγάλο", "Μαρούσι - μικρό"), None, -20),
	PairTeamRule(("Αγία Παρασκευή - μεγάλο", "Μαρούσι - μεγάλο"), "football", 10),
	LevelTeamRule("football", -2),
	LevelTeamRule("basketball", -3),
	LevelTeamRule("germaniko", -2),
]
