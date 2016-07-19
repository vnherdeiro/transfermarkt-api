#! /usr/bin/python


import urllib
import urllib2
from bs4 import BeautifulSoup
import re
from time import time

t1 = time()
url = "http://www.transfermarkt.co.uk/cristiano-ronaldo/leistungsdatenverein/spieler/8198"
#opener = urllib.request.build_opener()
#opener.addheaders = [('User-agent', 'Mozilla/5.0')]
inData = urllib2.Request(url, headers = {'User-agent': 'Mozilla/5.0'})
content = urllib2.urlopen(inData).read()
t2 = time()
print t2-t1
soup = BeautifulSoup( content, "html.parser")
t3 = time()
print t3-t2
#print soup.prettify()


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

clubsPlayedFor = set()
for link in soup.find_all("td", class_="hauptlink no-border-links"):
	clubsPlayedFor.add(	link.text)
print clubsPlayedFor
t4 = time()
print t4-t3
#print trophies
