#! /usr/bin/python3

#Class object scraping information about a player from URL and storing it


#improvement: adding more information -- performance over last season for instance

import urllib
from bs4 import BeautifulSoup
import re


class Player():

	def __init__(self, url):
		self.playerAttributes = {} #will store all the information in dictionnary

		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		inData = opener.open(url)
		content = inData.read()
		soup = BeautifulSoup( content, "html.parser")

		#retrieving picture url and basic name
		link = soup.find("div", {"class":"dataBild"})
		self.playerAttributes["Picture"] = link.img["src"]
		self.playerAttributes["Name"] = link.img["title"]

		#reading tabular info and storing
		for link in soup.find_all("table", {"class":"auflistung"}):
			for line in link.find_all("tr"):#, {"class" : "dataValue"}):
				text = re.sub("\r|\n|\t|\xa0|  ", "", line.text)
				lhs, rhs = text.split(":")
				if rhs:
					self.playerAttributes[lhs] = rhs

		#retrieving player value over career time graph and storing
		theXs = "".join( map(str, re.findall(b"'x':\d+",content)))
		theXs = list( map( lambda x : int(x)//1000, re.findall("\d+", theXs)))
		theYs = "".join( map(str, re.findall(b"'y':\d+",content)))
		theYs = list( map( int, re.findall("\d+", theYs)))
		if theYs:
			self.playerAttributes["Value"] = theYs[-1]
			self.playerAttributes["Value Graph"] = zip(theXs, theYs)
			#putting last value in printable form
			value = int(theYs[-1])
			valueString = ""
			while value:
				nextVal = value // 1000
				if nextVal:
					valueString = "," + "%03d" %(value % 1000) + valueString
				else:
					valueString = "£%d" %(value % 1000) + valueString
				value = nextVal
			self.playerAttributes["Printable Value"] = valueString

	def __getitem__(self, arg):
		return self.playerAttributes[arg] if arg in self.playerAttributes else "-" #or "n/a"


if __name__ == "__main__":

	#running check on Lord Eder
	url = "http://www.transfermarkt.co.uk/eder/profil/spieler/84481"
	thePlayer = Player(url)
	print(thePlayer.playerAttributes)
