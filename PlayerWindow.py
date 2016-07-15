#!/usr/bin/python3



import sys
from PyQt5.QtWidgets import (QWidget, QSlider,
	QLabel, QApplication, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import urllib
from bs4 import BeautifulSoup
import re
import Player

def downloadFile(url, fileName):
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	content = opener.open(url)
	with open(fileName,"b+w") as f:
		f.write(content.read())


class PlayerWindow(QWidget):

	def __init__(self, playerUrl):
		super().__init__()
		self.profile = Player.Player(playerUrl)
		self.initUI()


	def initUI(self):
		grid = QGridLayout()
		self.setLayout(grid)
		self.pictureLabel = QLabel()
		pictureFilename = "." + self.profile["Complete name"].lower().replace(" ","") + ".jpg"
		downloadFile(self.profile["Profile Picture"], pictureFilename)
		self.pictureLabel.setPixmap(QPixmap( pictureFilename))
		self.pictureLabel.adjustSize()
		grid.addWidget(self.pictureLabel,0,0,3,3)
		#self.label.setGeometry(160, 40, 80, 30)
		index = 3
		for key, value in self.profile.playerAttributes.items():
			if isinstance(value, (int,str)):
				lhs = QLabel()
				rhs = QLabel()
				lhs.setText( key)
				rhs.setText( str(value))
				grid.addWidget( lhs, index, 0)
				grid.addWidget( rhs, index, 1)
				index += 1
		self.setWindowTitle(self.profile["Name"])
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	url = "http://www.transfermarkt.co.uk/cristiano-ronaldo/profil/spieler/8198"
	ex = PlayerWindow(url)
	sys.exit(app.exec_())
