#!/usr/bin/python3

import sys
import playerSearch
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QTableView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import PlayerWindow
#function reading marker value from string for later ordering
import re

import glob
import os


def clearFolder():
	filesToDel = glob.glob(".*jpg")
	# print( filesToDel)
	for lFile in filesToDel:
		os.remove(lFile)

class QPlayerLabel(QLabel):

	def __init__(self, labelText, theUrl):
		self.playerUrl = theUrl
		super().__init__(labelText)

	def mousePressEvent(self, event):
		self.newWindow = PlayerWindow.PlayerWindow( self.playerUrl)
		self.newWindow.show()
		#print("window opened...")
		# newWindow.exec_()
		#input()

#need to add on click opening player window

def readVal(stringVal):
	value = float(re.findall("\d+.\d+", stringVal)[0])
	if stringVal[-1] == "m":
		value *= 10**6
	elif stringVal[-1] == "k":
		value *= 10**3
	return value

class SearchGui(QWidget):

	def __init__(self):
		super().__init__()

		#self.labelList = []
		self.initUI()

	def initUI(self):

		researchLabel = QLabel('Player Name')
		resultsLabel = QLabel('Search results')

		self.researchEdit = QLineEdit()
		#self.resultsEdit = QLabel()
		#self.resultsEdit = QLabel()
		#self.resultsEdit.setFont( QFont("Fira Mono Bold",12))
		#self.resultsEdit.setColumnCount(4)
		#self.resultsEdit.setRowCount(4)

		#self.resultsEdit.setFontPointSize(15)
		#self.resultsEdit.setAlignment(Qt.AlignRight)

		self.researchEdit.returnPressed.connect(self.newResearch)

		#self.resultsEdit = QGridLayout()
		self.grid = QGridLayout()
		self.grid.setSpacing(10)

		self.grid.addWidget(researchLabel, 1, 0)
		self.grid.addWidget(self.researchEdit, 1, 1)

		self.grid.addWidget(resultsLabel, 2, 0)
		#self.grid.addWidget(self.resultsEdit, 2, 1, 5, 1)

		self.setLayout(self.grid)

		self.setGeometry(100, 100, 1000, 400)
		self.setWindowTitle('Player Searcher')
		self.show()

	def newResearch(self):
		playerName = self.researchEdit.text()
		output = playerSearch.research( playerName)

		#clearing possible past entries
		while self.grid.count() > 3:
			item = self.grid.takeAt(3)
			widg = item.widget()
			widg.deleteLater()
	# for widg in self.labelList:
	# 		# widg.hide()
	# 		# widg.setParent(None)
	# 		self.grid.removeWidget(widg)
	# 		widg.deleteLater()
			# del widg
		#self.labelList = []
		if output:
			dicUrls, dicProperties = output
			#printing after ordering by decreasing market value
			index = 3
			for name, (age, club, value)  in sorted(dicProperties.items(), key = lambda x : readVal(x[-1][-1]))[::-1]:
				playerUrl = dicUrls[ name]
				labelText = "%-25s %2s %25s %8s" %(name, age, club, value)
				newLabel = QPlayerLabel(labelText, playerUrl)
				self.grid.addWidget(newLabel, index, 1)
				index += 1
			#self.resultsEdit.setText(newText)
			#self.resultsEdit.adjustSize()
		#else:
			#self.resultsEdit.setText("")


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = SearchGui()
	#sys.exit(app.exec_())
	app.exec_()
	# clearFolder()
