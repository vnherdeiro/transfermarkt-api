#!/usr/bin/python3

import sys
import playerSearch
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication)

from PyQt5.QtCore import Qt

class Example(QWidget):
	
	def __init__(self):
		super().__init__()
		
		self.initUI()
		
		
	def initUI(self):
		
		researchLabel = QLabel('Player Name')
		resultsLabel = QLabel('Search results')

		self.researchEdit = QLineEdit()
		self.resultsEdit = QLabel()

		#self.resultsEdit.setFontPointSize(15)
		self.resultsEdit.setAlignment(Qt.AlignRight)


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
			for name, (age, club, value)  in dicProperties.items():
				newText += "%-25s %2s %25s %8s\n\n" %(name, age, club, value)
			self.resultsEdit.setText(newText)
		else:
			self.resultsEdit.setText("")
			
		
if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
