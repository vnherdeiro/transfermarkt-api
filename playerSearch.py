#! /usr/bin/python3

#script returning (first 10) results of a player search


import urllib
#import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import os
import re
import datetime
from Player import Player
#import matplotlib.pylab as plt


opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
while True:
	name = str( input("Enter name for search:\t"))
	baseUrl = "http://www.transfermarkt.co.uk/schnellsuche/ergebnis/schnellsuche?query="
	baseProfileUrl = "http://www.transfermarkt.co.uk"
	url = baseUrl + name
	inData = opener.open(url)
	content = inData.read()
	soup = BeautifulSoup( content, "html.parser")
	dicPlayers = {}
	for link in soup.find_all("a", {"class" : "spielprofil_tooltip"}):
		dicPlayers[link.text] = Player(baseProfileUrl + link["href"])

	for name, player in dicPlayers.items():
		#print(player["Name"], "\t", player["Age"],"\t", player["Current club"], "\t", player["Printable Value"],"\t", player["Position"])
		print("\t%-40s %3s %40s %15s\t%-30s" %(player["Name"], player["Age"], player["Current club"], player["Printable Value"], player["Position"]))
