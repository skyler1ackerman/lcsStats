import requests, requests, urllib.parse, json
from bs4 import BeautifulSoup

URL = 'https://gol.gg/tournament/tournament-matchlist/LCS%20Spring%202021/'
BASEURL = 'https://gol.gg/'
PREFIX = '../'
FULL_STATS_SUFFIX = 'page-fullstats/'


# Takes the base URL (Should be constant) and returns the link to all completed games
def getLinks(url):
	basePage = requests.get(url)
	baseSoup = BeautifulSoup(basePage.content, features="html.parser")
	links = []
	for x in baseSoup.find_all('a'):
		link=x.get('href')
		if 'page-game' in link:
			links.append(BASEURL+link[link.startswith(PREFIX) and len(PREFIX):])
	return links

# Takes a link to a completed game and makes a new link with the suffix
def getStatsLink(link, suffix):
	return link[0:-10] + suffix

# Uses the link to find the game id
def getGameId(link):
	return link.split('/')[5]

# Uses the soup to get the game name
def getGameName(soup):
	return soup.find('h1').text

# Uses the soup to get the game length
def getGameLength(soup):
	return soup.find_all('h1')[1].text
	

def getGameDate(soup):
	return soup.find(class_='col-12 col-sm-5 text-right').text

# Takes the full stats url and uses it to get full data from the table
def getDetStats(URL):
	playerStats = {}
	detStatsPage = requests.get(URL)
	detStatsSoup = BeautifulSoup(detStatsPage.content, features="html.parser")
	tableRows = detStatsSoup.find('table').find_all('tr', recursive=False)
	for name in tableRows[0].find_all('td')[1:]:
		playerStats[name.text] = {}
	for row in tableRows[1:]:
		key = row.find('td').text
		for idx, stat in enumerate(row.find_all('td')[1:]):
			playerStats[list(playerStats.keys())[idx]][key] = stat.text
	return playerStats

def getAllData(url):
	gameData = {}
	links = getLinks(url)
	for link in links:
		tempDict = {}
		page = requests.get(link)
		gameSoup = BeautifulSoup(page.content, features="html.parser")
		gameID = getGameId(link)
		statsLink = getStatsLink(link, FULL_STATS_SUFFIX)
		tempDict['id'] = getGameId(link)
		tempDict['date'] = getGameDate(gameSoup)
		tempDict['playerStats'] = getDetStats(statsLink)
		gameData[getGameName(gameSoup)] = tempDict
	return gameData

# Write the data to the json file
# with open('data.json', 'w', indent=4) as outfile:
# 	json.dump(getAllData(URL), outfile)
tempUrl = 'https://gol.gg/game/stats/29003/page-game/'
page = requests.get(tempUrl)
gameSoup = BeautifulSoup(page.content, features="html.parser")
for table in gameSoup.find_all(class_='playersInfosLine footable toggle-square-filled'):
	for row in table.find_all('tr', recursive=False):
		print(row.find('img').get('alt'))