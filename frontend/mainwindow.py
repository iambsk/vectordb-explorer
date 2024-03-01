from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QGraphicsView, QTreeView, QListView, QFileDialog, QMenuBar, QMenu, QAction
from PyQt5 import uic
import sys

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		# load the ui file
		uic.loadUi("mainwindow.ui", self)

		# defs from ui file
		self.searchBar = self.findChild(QLineEdit , "searchBar")
		self.graphicsView = self.findChild(QGraphicsView, "graphicsView")
		self.treeView = self.findChild(QTreeView, "treeView")
		self.listView = self.findChild(QListView, "listView")

		self.menubar = self.findChild(QMenuBar, "menubar")
		self.menuFile = self.findChild(QMenu, "menuFile")
		self.actionNew = self.findChild(QAction, "actionNew")
		self.menuView = self.findChild(QMenu, "menuView")

		# connect
		self.searchBar.setPlaceholderText("Search")
		self.actionNew.triggered.connect(self.openFileDialog)


		self.show()

	def openFileDialog(self):
		options = QFileDialog.Options()
		fileName, _ = QFileDialog.getOpenFileName(None, "Open File", "", "All Files (*);;Text Files (*.  txt)", options=options)
		if fileName:
			print("Selected file:", fileName)


app = QApplication(sys.argv)
UIwindow = UI()
app.exec_()
