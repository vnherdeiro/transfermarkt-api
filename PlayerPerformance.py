#! /usr/bin/python3


import urllib
from bs4 import BeautifulSoup
import re

#cleans a string of excessive spaces and newlines
def cleanString(theString):
	return re.sub("\r|\n|\t|\xa0|  ", "", theString)


class PlayerPerformanceData():

	def __init__( self, playerUrl):
		self.url = playerUrl.replace("profil", "leistungsdaten") #url of the performance page

		opener = urllib.request.build_opener()
		opener.addheaders = [ ('User-agent', 'Mozilla/5.0')]
		content = opener.open(self.url).read()
		soup = BeautifulSoup( content, "lxml")

		#non exhaustive trophy list
		self.trophies = {}
		linkTrophies = soup.find("div", class_="dataErfolge show-for-small")
		for link in linkTrophies.find_all("div", class_="dataErfolg"): #soup.find_all("div", class_="dataErfolg"):
			try:
				self.trophies[ link.img["alt"]] = int( link.text.replace("\n",""))
			except:
				pass

		#collecting list of all clubs the player has played for
		self.clubsPlayedFor = []
		linkClubPerf = soup.find("div", class_="table-header", text="Performance per club").parent()[1]
		for line in linkClubPerf.find_all("td", class_="hauptlink no-border-links"):
			self.clubsPlayedFor.append( line.text)

		#reading career overall
		#first reading the position to know if goalkeeper or field player
		link = soup.find("span", class_="dataItem", text="Position:")
		link = link.parent()
		isKeeper = cleanString(link[1].text) == "Keeper"

		fieldPlayerStatsHeadSet = ["Games played", "Goals scored", "Assists", "Yellow cards", "YtoR cards", "Red cards"]
		goalkeeperStatsHeadSet = ["Games played", "Goals scored", "Yellow cards", "YtoR cards", "Red cards", "Goals suffered", "Clean sheets"]
		self.valTab = []
		self.valTitles = goalkeeperStatsHeadSet[:] if isKeeper else fieldPlayerStatsHeadSet[:]

		link = soup.find("tfoot")
		for line in link.find_all("td",class_="zentriert"):
			text = cleanString(line.text)
			if text == "-":
				self.valTab.append(0)
			else:
				self.valTab.append( int(text))

		link = soup.find("span", class_="dataItem", text="International caps/goals:")
		link = link.parent()
		self.international = link[1].text

		self.Summary = "Career Totals:\n"
		for entry, value in zip(self.valTitles, self.valTab):
			self.Summary += "\t%-30s\t%d\n" %(entry,value)
		self.Summary += "\nInternational caps/goals: %s" % self.international
		clubString = " -> ".join(club for club in self.clubsPlayedFor[::-1])
		self.Summary += "\n\nPlayed for:\t" + clubString
		self.Summary += "\n\nTrophy List (non-exhaustive):"
		for trophyEntry, trophyCount in self.trophies.items():
			self.Summary += "\n\t%-30s (%d)" %(trophyEntry, trophyCount)





if __name__ == "__main__":
	url = "http://www.transfermarkt.co.uk/cristiano-ronaldo/profil/spieler/8198"
	playerPerf = PlayerPerformanceData(url)
	# print( "Trophies won: (non exhaustive)")
	# for a,b in playerPerf.trophies.items():
	# 	print ("\t%-30s\t%d" %(a,b))
	# print ( "Played for:\t"," - ".join(club for club in playerPerf.clubsPlayedFor[::-1]))
	# for a,b in zip(playerPerf.valTitles, playerPerf.valTab):
	# 	print( "%-20s\t%d" %(a,b))
	# print ("International caps/goals:\t", playerPerf.international)
	print (playerPerf.Summary)

#eof
