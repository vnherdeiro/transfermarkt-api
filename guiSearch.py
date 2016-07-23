#!/usr/bin/python3

import sys
import PlayerSearch
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QTableView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import PlayerWindow
import re
import glob
import os


#clearing hidden images in folder
def clearFolder():
	filesToDel = glob.glob(".*jpg")
	for lFile in filesToDel:
		os.remove(lFile)

#object handling a player search result and opening player window when clicked on
class QPlayerLabel(QLabel):

	def __init__(self, labelText, theUrl):
		super().__init__(labelText)
		self.setStyleSheet("border : 1px solid gray; border-radius : 10px; background-color : #303030; color: white")
		self.setFont( QFont("Fira Mono Bold",12))
		self.playerUrl = theUrl

	def mousePressEvent(self, event):
		self.displayPlayerWindow()

	def displayPlayerWindow(self):
		newWindow = PlayerWindow.PlayerWindow( self.playerUrl)
		newWindow.show()
		self.newWindow = newWindow

#need to add on click opening player window

def readVal(stringVal):
	if stringVal == "-":
		return 0
	value = float(re.findall("\d+.\d+|\d+", stringVal)[0])
	if stringVal[-1] == "m":
		value *= 10**6
	elif stringVal[-1] == "k":
		value *= 10**3
	return value

class SearchWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		# self.setStyleSheet( "background-color : grey")
		researchLabel = QLabel('Player Name')
		researchLabel.setFont( QFont("Fira Mono Bold", 11))
		researchLabel.adjustSize()
		resultsLabel = QLabel('Search results')
		resultsLabel.setFont( QFont("Fira Mono Bold", 11))
		resultsLabel.adjustSize()

		researchEdit = QLineEdit()
		researchEdit.setStyleSheet( "border : 2px solid #75FF6961; border-radius : 5px; background-color : #cbcbcb")
		researchEdit.setFont( QFont("Fira Mono Bold",12))
		researchEdit.returnPressed.connect(self.newResearch)

		grid = QGridLayout()
		grid.setSpacing(4)
		grid.addWidget(researchLabel, 1, 0)
		grid.addWidget(researchEdit, 1, 1)
		grid.addWidget(resultsLabel, 2, 0)
		self.setLayout(grid)
		self.setGeometry(100, 100, 1000, 400)
		self.setWindowTitle('Player Searcher')
		self.show()

		self.researchEdit = researchEdit
		self.grid = grid

	def newResearch(self):
		playerName = self.researchEdit.text()
		output = PlayerSearch.research( playerName)

		#clearing possible past entries
		while self.grid.count() > 3:
			item = self.grid.takeAt(3)
			widg = item.widget()
			widg.deleteLater()

		#displaying new output
		if output:
			dicUrls, dicProperties = output
			#printing after ordering by decreasing market value
			index = 3
			for name, (age, club, value)  in sorted(dicProperties.items(), key = lambda x : readVal(x[-1][-1]))[::-1]:
				playerUrl = dicUrls[ name]
				labelText = "%-25s %2s %25s %8s" %(name, age, club, value)
				newLabel = QPlayerLabel(labelText, playerUrl)
				self.grid.addWidget(newLabel, index, 1, Qt.AlignTop)
				index += 1
			#self.resultsEdit.adjustSize()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = SearchWindow()
	sys.exit( app.exec_())

#eof
