import json
with open('data.json') as json_file:
    fullData = json.load(json_file)

#  This returns the highest stat of the season for a given catagory
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
	return {k:v[0]/v[1] for k, v in playerStats.items()}

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

def initAllStats():
	return {k:{} for k in fullData['EG vs CLG']['playerStats']['Impact'].keys()}
def whatbest():
	playerStats = initAllStats()
	for game, gameData in fullData.items():
		for player, stats in gameData['playerStats'].items():

			for statKey, stat in stats.items():
				try:
					if player in playerStats[statKey].keys():
						if playerStats[statKey][player][0] < float(stat):
							playerStats[statKey][player] = [float(stats[statKey]), game, gameData['date']]
					else:
						playerStats[player] = [float(stats[statKey]), game, gameData['date']]
				except ValueError:
					pass
	return playerStats

def addStat(stat):
	playerStats = {}
	for game in fullData.values():
		for player, stats in game['playerStats'].items():
			if player in playerStats.keys():
				playerStats[player] += float(stats[stat])
			else:
				playerStats[player] = float(stats[stat])
	return playerStats

def indPoints(indv):
	points = 0
	pointStats = [('Kills', 3), ('Deaths', -1), ('Assists', 2), ('CS', .01)]
	for tup in pointStats:
		points+=addStat(tup[0])[indv]*tup[1]
	return points

# stats = avgStat(addStatRole('Vision Score', 'SUPPORT'))

# ecoList = ['CS', 'CSM', 'CS in Team\'s Jungle', "CS in Enemy Jungle", 'GD@15', "Golds", "GPM"]
allKeys = ['Role', 'Kills', 'Deaths', 'Assists', 'KDA', 'CS', "CS in Team's Jungle", 'CS in Enemy Jungle', \
'CSM', 'Golds', 'GPM', 'GOLD%', 'Vision Score', 'Wards placed', 'Wards destroyed', 'Control Wards Purchased', \
'VSPM', 'WPM', 'VWPM', 'WCPM', 'VS%', 'Total damage to Champion', 'Physical Damage', 'Magic Damage', 'True Damage',\
 'DPM', 'DMG%', 'K+A Per Minute', 'KP%', 'Solo kills', 'Double kills', 'Triple kills', 'Quadra kills', 'Penta kills', \
 'GD@15', 'CSD@15', 'XPD@15', 'LVLD@15', 'Damage dealt to turrets', 'Total heal', 'Damage self mitigated', 'Time ccing others', \
 'Total damage taken']

allPlayerPoints = {}
for name in addStat('Kills').keys():
	allPlayerPoints[name]=indPoints(name)
allPlayerPoints = {k: v for k, v in sorted(allPlayerPoints.items(), key=lambda item: item[1])}

for k, v in allPlayerPoints.items():
	print(k +': '+ str(v))


# allStatsDict = {}
# for statKey in allKeys:
# 	try:
# 		stats = addStat(statKey)
# 		stats = {k: v for k, v in sorted(stats.items(), key=lambda item: item[1])}
# 		allStatsDict[statKey] = stats
# 	except ValueError:
# 		pass

# idx = -1
# # print(json.dumps(allStatsDict,indent=4))
# for statsKey, stats in allStatsDict.items():
# 	print(statsKey, list(stats.keys())[idx], stats[list(stats.keys())[idx]])

# print(', '.join(fullData['EG vs CLG']['playerStats']['Impact'].keys()))