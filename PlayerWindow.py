#!/usr/bin/python3

#window scrapping and showing player information

import sys

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (QSizePolicy, QWidget, QSlider, QLabel, QApplication, QGridLayout, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import urllib
from bs4 import BeautifulSoup
import re
import Player
import os
from datetime import datetime
from PlayerPerformance import PlayerPerformanceData

#downloads and stores file -- used to download player profile picture
def downloadFile(url, fileName):
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	content = opener.open(url)
	with open(fileName,"b+w") as f:
		f.write( content.read())

class ValueGraph(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, data, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)
		# We want the axes cleared every time plot() is called
		self.axes.hold(False)
		self.xData, self.yData = zip(*data)
		self.xData = list( map( lambda x : datetime.fromtimestamp( x), self.xData))
		self.yData = list( map( lambda x : x / 10**6, self.yData))
		self.drawGraph()

		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def drawGraph(self):
		self.axes.set_axis_bgcolor(".85")
		self.axes.plot(self.xData, self.yData, marker="o", lw=2, c="#1c798e")
		maxVal = max( self.yData)
		self.axes.axhline(y= maxVal, c="orange", ls="--", lw=1.5)
		self.axes.grid( True)
		self.axes.set_title("Player value over career years", fontsize=10)
		self.axes.set_ylabel("Million £", fontsize=9)
		#self.fig.tight_layout() -- bugged and useless here

class PerformanceButton(QPushButton):

	def __init__(self, textLink, playerUrl):
		self.textLink = textLink
		self.playerUrl = playerUrl
		super().__init__()
		self.clicked.connect(self.buttonClicked)

	def buttonClicked(self):
		perfData = PlayerPerformanceData(self.playerUrl)
		self.textLink.setText( perfData.Summary)
		self.textLink.show()
		self.hide()

class PlayerWindow(QWidget):

	def __init__(self, playerUrl):
		super().__init__()
		self.playerUrl = playerUrl
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
		downloadFile(self.profile["Picture"], self.pictureFilename)
		self.pictureLabel.setPixmap( QPixmap( self.pictureFilename))
		self.pictureLabel.adjustSize()
		grid.addWidget(self.pictureLabel,0,0,3,3)
		#self.label.setGeometry(160, 40, 80, 30)
		index = 3
		for key, value in self.profile.playerAttributes.items():
			if isinstance(value, (int,str)) and key != "Picture" and key != "Value (int)":
				lhs = QLabel()
				rhs = QLabel()
				lhs.setText( key)
				rhs.setText( str(value))
				grid.addWidget( lhs, index, 0, Qt.AlignTop)
				grid.addWidget( rhs, index, 1, Qt.AlignTop)
				index += 1
		theGraph = ValueGraph( self.profile["Value Graph"], QWidget(self), width=5, height=4, dpi=100)
		grid.addWidget(theGraph, index, 0, 3, 3, Qt.AlignTop)
		index += 3
		perfText = QLabel()
		grid.addWidget( perfText, index, 0, 3, 3, Qt.AlignCenter)
		perfText.hide()
		perfButton = PerformanceButton( perfText, self.playerUrl)
		perfButton.setText("Show %s performance data" %(self.profile["Name"]))
		index += 3
		grid.addWidget( perfButton, index, 0, 1, 3, Qt.AlignCenter)
		self.setWindowTitle( self.profile["Name"])
		self.show()

	def keyPressEvent(self, e): #closes on Esc press
		if e.key() == Qt.Key_Escape:
			self.close()

	def __del__(self):
		print ("\t\t\tcall destructor")
		if os.path.isfile( self.pictureFilename):
			os.remove( self.pictureFilename)
		del self.profile
		del self.pictureLabel


if __name__ == '__main__':
	app = QApplication( sys.argv)
	url = "http://www.transfermarkt.co.uk/cristiano-ronaldo/profil/spieler/8198"
	ex = PlayerWindow( url)
	sys.exit( app.exec_())
