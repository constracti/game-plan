# game-plan

## configuration

set games, teams and rules in `config.py`

## search

search for game plans according to `games` and `grules` (game rules) with `search.py`

### example

```
python3 search.py --stop 2 --outfile plans.txt
```

## assign

test team permutations according to `games`, `teams` and `trules` (team rules) with `assign.py`

### example

```
python3 assign.py --score 10. --infile plans.txt --outfile solution.txt
```

## export

export csv files with `games.py` and `teams.py`

### example

```
python3 games.py --infile solution.txt --outfile games.csv
```

```
python3 teams.py --infile solution.txt --outfile teams.csv
```
