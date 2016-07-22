#! /usr/bin/python3


import urllib
from bs4 import BeautifulSoup
import re
from time import time


#TO BE ADDED:
#			- individual and club trophies X
#			- history of clubs played for X
#			- performance over last season => REQUIRES TO LOAD ANOTHER PAGE....
#			- differentiate goalkeepers X
#			- internional caps / performance (fix missing space in multiple citizenship) X
#			- carreer overall performance X
#
#			- then fit everything inside a class and add information to player window -- maybe using a hide/show panel !!!!!!


t1 = time()
url = "http://www.transfermarkt.co.uk/cristiano-ronaldo/leistungsdatenverein/spieler/8198"
# url = "http://www.transfermarkt.co.uk/rui-patricio/leistungsdaten/spieler/45026"
opener = urllib.request.build_opener()
opener.addheaders = [ ('User-agent', 'Mozilla/5.0')]
content = opener.open(url).read()
t2 = time()
print( t2-t1)
soup = BeautifulSoup( content, "html.parser")
t3 = time()
print( t3-t2)
#print soup.prettify()

#cleans a string of excessive spaces and newlines
def cleanString(theString):
	return re.sub("\r|\n|\t|\xa0|  ", "", theString)

#missing some trophies here...
trophies = {}
linkTrophies = soup.find("div", class_="dataErfolge show-for-small")
for link in linkTrophies.find_all("div", class_="dataErfolg"): #soup.find_all("div", class_="dataErfolg"):
	try:
		trophies[ link.img["alt"]] = int( link.text.replace("\n",""))
	except:
		pass

print( "Trophies won: (non exhaustive)")
for a,b in trophies.items():
	print ("\t%-30s\t%d" %(a,b))
	#print link.prettify(),"\n\n\n"

for link in soup.find_all("div", class_="dataDaten"):
	# print link.prettify()
	continue

#collecting list of all clubs the player has played for
clubsPlayedFor = []
#redundancy here in collecting the club information
for link in soup.find_all("td", class_="hauptlink no-border-links"):
	if link.text not in clubsPlayedFor: #this insures that they are stored in inverse career order
		clubsPlayedFor.append( link.text)

print ( "Played for:\t"," - ".join(club for club in clubsPlayedFor[::-1]))
# print clubsPlayedFor

#now collecting goal information

#club teammates information
# link = soup.find("select", {"data-placeholder":"Player(s)"})
# for l in link.find_all("option"):
# 	print l.text

#league clubs information
# link = soup.find("select", {"data-placeholder":"Club(s)"})
# for l in link.find_all("option"):
# 	print l.text

# link = soup.find("table", class_="items")
# for data in link.find_all("td", class_="zentriert"):
# 	print( cleanString(data.text))


#reading career overall

#first reading the position to know if goalkeeper or field player
link = soup.find("span", class_="dataItem", text="Position:")
link = link.parent()
isKeeper = cleanString(link[1].text) == "Keeper"

fieldPlayerStatsHeadSet = ["Games played", "Goals scored", "Assists", "Yellow cards", "YtoR cards", "Red cards"]
goalkeeperStatsHeadSet = ["Games played", "Goals scored", "Yellow cards", "YtoR cards", "Red cards", "Goals suffered", "Clean sheets"]

link = soup.find("tfoot")
valTab = []

valTitles = goalkeeperStatsHeadSet[:] if isKeeper else fieldPlayerStatsHeadSet[:]
for line in link.find_all("td",class_="zentriert"):
	text = cleanString(line.text)
	if text == "-":
		valTab.append(0)
	else:
		valTab.append( int(text))

for a,b in zip(valTitles,valTab):
	print( "%-20s\t%d" %(a,b))

link = soup.find("span", class_="dataItem", text="International caps/goals:")
link = link.parent()
print ("International caps/goals:\t", link[1].text)


t4 = time()
print( t4-t3)
#print trophies

#eof
