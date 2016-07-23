#! /usr/bin/python3

#script returning (first 10) results of a player search


import urllib
from bs4 import BeautifulSoup
import re
#import datetime

#our class handling players
from Player import Player



#searches for players
def research(playerName):
	try:
		baseUrl = "http://www.transfermarkt.co.uk/schnellsuche/ergebnis/schnellsuche?query="
		baseProfileUrl = "http://www.transfermarkt.co.uk"
		url = baseUrl + playerName
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		inData = opener.open(url)
		content = inData.read()
		soup = BeautifulSoup( content, "html.parser")
		dicPlayers = {}
	#	for link in soup.find_all("a", {"class" : "spielprofil_tooltip"}):
	#		dicPlayers[link.text] = Player(baseProfileUrl + link["href"])
	#
	#	for name, player in dicPlayers.items():
	#		#print(player["Name"], "\t", player["Age"],"\t", player["Current club"], "\t", player["Printable Value"],"\t", player["Position"])
	#		print("\t%-35s %2s %35s %13s\t%-30s" %(player["Name"], player["Age"], player["Current club"], player["Printable Value"], player["Position"]))
	#

		#quickerSearch
		dicUrls = {}
		dicAttributes = {}
		for name, age, club, value in zip( soup.find_all("a", {"class":"spielprofil_tooltip"}), soup.find_all("td", class_ = "zentriert", text=re.compile("\d+")), soup.find_all("img", {"class":"tiny_wappen"}),soup.find_all("td", class_ = "rechts hauptlink")):
			#print( "\t%25s %2s %-35s %8s" %(name.text, age.text, club["alt"],value.text))
			dicUrls[name.text] = baseProfileUrl + name["href"]
			dicAttributes[name.text] = (age.text, club["alt"], value.text)
		return dicUrls, dicAttributes
	except:
		return None

if __name__ == "__main__":
	while True:
		name = str( input("Enter name for search:\t"))
		output = research( name)
		if output:
			dicUrls, dicProperties = output
			for name, (age, club, value)  in dicProperties.items():
				print( "\t%25s %2s %-35s %8s" %(name, age, club, value))
