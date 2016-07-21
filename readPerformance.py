#! /usr/bin/python3


import urllib
from bs4 import BeautifulSoup
import re
from time import time

t1 = time()
url = "http://www.transfermarkt.co.uk/cristiano-ronaldo/leistungsdatenverein/spieler/8198"
opener = urllib.request.build_opener()
#opener.addheaders = [('User-agent', 'Mozilla/5.0')]
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
content = opener.open(url).read()
t2 = time()
print(t2-t1)
soup = BeautifulSoup( content, "html.parser")
t3 = time()
print(t3-t2)
#print soup.prettify()

#cleans a string of excessive spaces and newlines
def cleanString(theString):
	return re.sub("\r|\n|\t|\xa0|  ", "", theString)

trophies = {}
for link in soup.find_all("div", class_="dataErfolg"):
	try:
		#print link.img["alt"], link.text.replace("\n","")
		trophies[ link.img["alt"]] = int(link.text.replace("\n",""))
	except:
		pass
	#print link.prettify(),"\n\n\n"

for link in soup.find_all("div", class_="dataDaten"):
	# print link.prettify()
	continue

#collecting list of all clubs the player has played for
clubsPlayedFor = set()
#redundancy here in collecting the club information
for link in soup.find_all("td", class_="hauptlink no-border-links"):
	clubsPlayedFor.add(	link.text)
# print clubsPlayedFor

#now collecting goal information

#club teammates information
link = soup.find("select", {"data-placeholder":"Player(s)"})
# for l in link.find_all("option"):
# 	print l.text

#league clubs information
link = soup.find("select", {"data-placeholder":"Club(s)"})
# for l in link.find_all("option"):
# 	print l.text

link = soup.find("table", class_="items")
for data in link.find_all("td", class_="zentriert"):
	print(cleanString(data.text))

t4 = time()
print(t4-t3)
#print trophies
