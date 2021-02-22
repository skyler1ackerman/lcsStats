import json
with open('data.json') as json_file:
    fullData = json.load(json_file)

def addStat(stat):
	playerStats = {}
	for game in fullData.values():
		for player, stats in game['playerStats'].items():
			if player in playerStats.keys():
				playerStats[player] += float(stats[stat])
			else:
				playerStats[player] = float(stats[stat])
	return playerStats

def highStat(stat):
	playerStats = {}
	for game, gameData in fullData.items():
		for player, stats in gameData['playerStats'].items():
			if player in playerStats.keys():
				if playerStats[player][0] < float(stats[stat]):
					playerStats[player] = [float(stats[stat]), game, gameData['date']]
			else:
				playerStats[player] = [float(stats[stat]), game, gameData['date']]
	return playerStats

def lowStat(stat):
	playerStats = {}
	for game, gameData in fullData.items():
		for player, stats in gameData['playerStats'].items():
			if player in playerStats.keys():
				if playerStats[player][0] > float(stats[stat]):
					playerStats[player] = [float(stats[stat]), game, gameData['date']]
			else:
				playerStats[player] = [float(stats[stat]), game, gameData['date']]
	return playerStats

def avgStat(stat):
	playerStats = {}
	for game in fullData.values():
		for player, stats in game['playerStats'].items():
			if player in playerStats.keys():
				playerStats[player][0] += float(stats[stat])
				playerStats[player][1] += 1
			else:
				playerStats[player] = [float(stats[stat]), 1]
	return playerStats

def addStatRole(stat, role):
	playerStats = {}
	for game in fullData.values():
		for player, stats in game['playerStats'].items():
			if stats['Role'] == role:
				if player in playerStats.keys():
					playerStats[player][0] += float(stats[stat])
					playerStats[player][1] += 1
				else:
					playerStats[player] = [float(stats[stat]), 1]
	return playerStats

def avgStatOut(statDict):
	return {k:(v[0]/v[1]) for k,v in statDict.items()}

def avgLeague(statsDict):
	total = 0
	for k, v in statsDict.items():
		total += v[0]
	return total/len(statsDict)

aliasDict = {'sup':'SUPPORT', 'Suport': 'SUPPORT'}
# stats = avgStat(addStatRole('Vision Score', 'SUPPORT'))
stats = lowStat('GD@15')

stats = {k: v for k, v in sorted(stats.items(), key=lambda item: item[1])}
for k, x in stats.items():
	print(k, x)
