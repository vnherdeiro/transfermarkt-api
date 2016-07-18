#!/usr/bin/python3

#window scrapping and showing player information

import sys
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import urllib
from bs4 import BeautifulSoup
import re
import Player
import os

#downloads and stores file -- used to download player profile picture
def downloadFile(url, fileName):
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	content = opener.open(url)
	with open(fileName,"b+w") as f:
		f.write( content.read())


class PlayerWindow(QWidget):

	def __init__(self, playerUrl):
		super().__init__()
		self.profile = Player.Player(playerUrl)
		self.initUI()


	def initUI(self):
		grid = QGridLayout()
		self.setLayout(grid)
		self.pictureLabel = QLabel()
		if self.profile["Complete name"] != "-":
			self.pictureFilename = "." + self.profile["Complete name"].lower().replace(" ","") + ".jpg"
		else:
			self.pictureFilename = "." + self.profile["Name"].lower().replace(" ","") + ".jpg"
		# print(self.pictureFilename)
		downloadFile(self.profile["Profile Picture"], self.pictureFilename)
		self.pictureLabel.setPixmap(QPixmap( self.pictureFilename))
		self.pictureLabel.adjustSize()
		grid.addWidget(self.pictureLabel,0,0,3,3)
		#self.label.setGeometry(160, 40, 80, 30)
		index = 3
		for key, value in self.profile.playerAttributes.items():
			if isinstance(value, (int,str)) and key != "Profile Picture":
				lhs = QLabel()
				rhs = QLabel()
				lhs.setText( key)
				rhs.setText( str(value))
				grid.addWidget( lhs, index, 0)
				grid.addWidget( rhs, index, 1)
				index += 1
		self.setWindowTitle( self.profile["Name"])
		self.show()

	def keyPressEvent(self, e): #closes on Esc press
		if e.key() == Qt.Key_Escape:
			self.close()

	def __del__(self):
		if os.path.isfile(self.pictureFilename):
			os.remove(self.pictureFilename)

if __name__ == '__main__':
	app = QApplication( sys.argv)
	url = "http://www.transfermarkt.co.uk/cristiano-ronaldo/profil/spieler/8198"
	ex = PlayerWindow( url)
	sys.exit( app.exec_())
