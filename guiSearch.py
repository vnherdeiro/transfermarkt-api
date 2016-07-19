#!/usr/bin/python3

import sys
import playerSearch
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
		self.playerUrl = theUrl
		super().__init__(labelText)

	def mousePressEvent(self, event):
		self.newWindow = PlayerWindow.PlayerWindow( self.playerUrl)
		self.newWindow.show()

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

		#self.labelList = []
		self.initUI()

	def initUI(self):

		researchLabel = QLabel('Player Name')
		resultsLabel = QLabel('Search results')

		self.researchEdit = QLineEdit()
		#self.resultsEdit.setFont( QFont("Fira Mono Bold",12))
		#self.resultsEdit.setFontPointSize(15)
		#self.resultsEdit.setAlignment(Qt.AlignRight)

		self.researchEdit.returnPressed.connect(self.newResearch)

		self.grid = QGridLayout()
		self.grid.setSpacing(4)

		self.grid.addWidget(researchLabel, 1, 0)
		self.grid.addWidget(self.researchEdit, 1, 1)

		self.grid.addWidget(resultsLabel, 2, 0)

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
	#		del widg
		#self.labelList = []
		if output:
			dicUrls, dicProperties = output
			#printing after ordering by decreasing market value
			index = 3
			# print(dicProperties)
			for name, (age, club, value)  in sorted(dicProperties.items(), key = lambda x : readVal(x[-1][-1]))[::-1]:
				playerUrl = dicUrls[ name]
				labelText = "%-25s %2s %25s %8s" %(name, age, club, value)
				newLabel = QPlayerLabel(labelText, playerUrl)
				newLabel.setFont( QFont("Fira Mono Bold",12))
				self.grid.addWidget(newLabel, index, 1, Qt.AlignTop)
				index += 1
			#self.resultsEdit.adjustSize()

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.close()

	def __del__(self):
		del self.grid
		del self.researchEdit

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = SearchWindow()
	sys.exit( app.exec_())
