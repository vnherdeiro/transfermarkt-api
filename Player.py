#! /usr/bin/python3

#Class object scraping information about a player from URL and storing it


#improvement: adding more information -- performance over last season for instance

import urllib
from bs4 import BeautifulSoup
import re


class Player():

	def __init__(self, url):
		playerAttributes = {} #will store all the information in dictionnary

		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		inData = opener.open(url)
		content = inData.read()
		soup = BeautifulSoup( content, "html.parser")

		#retrieving picture url and basic name
		link = soup.find("div", {"class":"dataBild"})
		playerAttributes["Picture"] = link.img["src"]
		playerAttributes["Name"] = link.img["title"]

		#reading tabular info and storing
		for link in soup.find_all("table", {"class":"auflistung"}):
			for line in link.find_all("tr"):#, {"class" : "dataValue"}):
				text = re.sub("\r|\n|\t|\xa0|  ", "", line.text)
				lhs, rhs = text.split(":")
				if rhs:
					playerAttributes[lhs] = rhs

		#retrieving player value over career time graph and storing
		theXs = [ int(_)//1000 for _ in re.findall( b"'x':(\d+)", content)]
		theYs = [ int(_) for _ in re.findall( b"'y':(\d+)", content)]
		if theYs:
			value = theYs[-1]
			playerAttributes["Value (int)"] = value
			playerAttributes["Value Graph"] = zip(theXs, theYs)
			#putting actual player market value in printable form
			valueString = ""
			while value:
				nextVal = value // 1000
				if nextVal:
					valueString = "," + "%03d" %(value % 1000) + valueString
				else:
					valueString = "£%d" %(value % 1000) + valueString
				value = nextVal
			playerAttributes["Market Value"] = valueString
		self.playerAttributes = playerAttributes

	def __getitem__(self, arg):
		return self.playerAttributes[arg] if arg in self.playerAttributes else "-" #or "n/a"


if __name__ == "__main__":
	#running check on Lord Eder
	url = "http://www.transfermarkt.co.uk/eder/profil/spieler/84481"
	thePlayer = Player(url)
	print(thePlayer.playerAttributes)

#eof
