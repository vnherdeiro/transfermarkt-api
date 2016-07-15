#!/usr/bin/python3

import sys
import playerSearch
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QTableView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


#function reading marker value from string for later ordering
import re
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

		self.initUI()


	def initUI(self):

		researchLabel = QLabel('Player Name')
		resultsLabel = QLabel('Search results')

		self.researchEdit = QLineEdit()
		#self.resultsEdit = QLabel()
		self.resultsEdit = QLabel()
		self.resultsEdit.setFont( QFont("Fira Mono Bold",12))
		#self.resultsEdit.setColumnCount(4)
		#self.resultsEdit.setRowCount(4)

		#self.resultsEdit.setFontPointSize(15)
		#self.resultsEdit.setAlignment(Qt.AlignRight)

		self.researchEdit.returnPressed.connect(self.newResearch)

		grid = QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(researchLabel, 1, 0)
		grid.addWidget(self.researchEdit, 1, 1)

		grid.addWidget(resultsLabel, 2, 0)
		grid.addWidget(self.resultsEdit, 2, 1, 5, 1)

		self.setLayout(grid)

		self.setGeometry(100, 100, 1000, 400)
		self.setWindowTitle('Player Searcher')
		self.show()

	def newResearch(self):
		playerName = self.researchEdit.text()
		output = playerSearch.research( playerName)
		if output:
			dicUrls, dicProperties = output
			newText = ""
			#printing after ordering by decreasing market value
			for name, (age, club, value)  in sorted(dicProperties.items(), key = lambda x : readVal(x[-1][-1]))[::-1]:
				newText += "%-25s %2s %25s %8s\n" %(name, age, club, value)
			self.resultsEdit.setText(newText)
			self.resultsEdit.adjustSize()
		else:
			self.resultsEdit.setText("")


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = SearchGui()
	sys.exit(app.exec_())
