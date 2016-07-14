#! /usr/bin/python3

#python3 version
import urllib
#import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import os
import re
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
url = "http://www.transfermarkt.co.uk/hatem-ben-arfa/profil/spieler/18900"
inData = opener.open(url)
#print(inData.read())
#with open("TODEL","w") as f:
#	f.write(inData.read())
soup = BeautifulSoup( inData, "html.parser")
#print(soup.prettify())
#for link in soup.find_all('a'):
#print link.get('href')

#for link in soup.table.find_all("a"):
#	text = link.prettify()
#	if "magnet" in text and "may" in text and "g6" in text and "okc" in text and "720" in text and not "60fps" in text:
#		print(link["href"]+"\n\n")
#		theLink = link["href"]
#		os.system("transmission-gtk \"" + theLink + "\"")
#		sys.exit()

playerAttributes = []
for link in soup.find_all("div",{"class" : "dataContent"}):
	#print( link.prettify() + "\n\n\n")
	for line in link.find_all("span", {"class" : "dataValue"}):
		#print(line.class)
		#playerAttributes.append(line.text.replace("\r","").replace("\n","").replace("  ",""))
		playerAttributes.append(re.sub("\r|\n|  ", "", line.text))
		#print(line.getText())
print(playerAttributes)

