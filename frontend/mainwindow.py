from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QStackedWidget, QTreeView, QListView, QFileDialog, QMenuBar, QMenu, QAction, QSplitter, QFileSystemModel
from PyQt5 import uic
import os
from typing import List

import backend.src.backend as backend
from backend.src.backend.types import Document
from backend.src.backend.client import FileDBClient

filedb = backend.fileio.FileDB(folder="../sample/sample_files",chroma_dir="../sample/chroma")
# filedb = FileDBClient()
class DocumentStandardItemModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setItemData(self, index, data):
        item = self.itemFromIndex(index)
        item.setData(data, QtCore.Qt.UserRole)

        self.show()

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.documents: List[Document] = []
        # load the ui file
        uic.loadUi("mainwindow.ui", self)

        # defs from ui file
        self.searchBar = self.findChild(QLineEdit , "searchBar")
        self.graphicsView = self.findChild(QStackedWidget, "stackedWidget")
        self.treeView = self.findChild(QTreeView, "treeView")
        self.listView = self.findChild(QListView, "listView")
        self.listView.doubleClicked.connect(self.searchItemDoubleClicked)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # Removes the ability to double click and edit

        # Adding file system tree view
        self.model = QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.rootPath())  # Or any specific path you want to show

        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(QtCore.QDir.rootPath()))  # Adjust if you're using a specific path      
        # Optional: Customize the view
        self.treeView.hideColumn(1)  # Example: Hide the size column
        self.treeView.hideColumn(2)  # Hide the type column
        self.treeView.hideColumn(3)  # Hide the date modified column
        
        
        self.splitter = self.findChild(QSplitter, "splitter")       
        self.menubar = self.findChild(QMenuBar, "menubar")
        self.menuFile = self.findChild(QMenu, "menuFile")
        self.actionNew = self.findChild(QAction, "actionNew")
        self.menuView = self.findChild(QMenu, "menuView")

        # connect
        self.splitter.setSizes([50, 100, 50])
        self.searchBar.setPlaceholderText("Search")
        self.searchBar.returnPressed.connect(self.searchList)
        self.actionNew.triggered.connect(self.openFileDialog)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openContextMenu)

        folderIndex = self.model.index(filedb.folder)
        self.treeView.expand(folderIndex)

        self.treeView.scrollTo(folderIndex, QTreeView.EnsureVisible)

        # INIT LIST VIEW
        
        # self.listView = QtWidgets.QListView(self.widget2)   
        # self.listView.setObjectName("listView")
        # self.listView.doubleClicked.connect(self.searchItemDoubleClicked)
        # self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # Removes the ability to double click and edit

        # self.verticalLayout.addWidget(self.listView)
        # model = QtGui.QStandardItemModel()
        # self.listView.setModel(model)
        
        # self.horizontalLayout.addWidget(self.splitter)
        # MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        # self.menubar.setObjectName("menubar")
        # self.menuFile = QtWidgets.QMenu(self.menubar)
        # self.menuFile.setObjectName("menuFile")
        # self.menuView = QtWidgets.QMenu(self.menubar)
        # self.menuView.setObjectName("menuView")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        # self.actionNew = QtWidgets.QAction(MainWindow)
        # self.actionNew.setObjectName("actionNew")
        # self.actionNew.triggered.connect(self.openFileDialog)
        # self.actionExit = QtWidgets.QAction(MainWindow)
        # self.actionExit.setObjectName("actionExit")
        # self.menuFile.addAction(self.actionNew)
        # self.menubar.addAction(self.menuFile.menuAction())
        # self.menubar.addAction(self.menuView.menuAction())


    def deleteSelectedFiles(self):
        indexes = self.treeView.selectedIndexes()
        if indexes:
            confirm = QtWidgets.QMessageBox.question(self, "Delete File",
                                                     "Are you sure you want to delete the selected file(s)?",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirm == QtWidgets.QMessageBox.Yes:
                for index in indexes:
                    if self.model.isDir(index):
                        continue  # Skip directories or implement directory deletion logic
                    file_path = self.model.filePath(index)
                    os.remove(file_path)
                    # Optionally, refresh the QFileSystemModel or parent directory to reflect the deletion
                    self.model.removeRow(index.row(), index.parent())

    def openContextMenu(self, position):
        contextMenu = QMenu(self)
        deleteAction = contextMenu.addAction("Delete File")
        action = contextMenu.exec_(self.treeView.viewport().mapToGlobal(position))
        if action == deleteAction:
            self.deleteSelectedFiles()

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print("Selected file:", fileName)
            filedb.add_file(fileName)
            self.searchList()
           
    def searchList(self):
        text = self.searchBar.text()
        # Dummy list for demonstration
        self.documents = filedb.vector_search(query_texts=[text],n_results=10)
        
        # Filter the list based on the search text
        # searched_text = [item.text for item in self.documents]

        # Update the list view
        model = DocumentStandardItemModel()
        for document in self.documents:
            model_item = QtGui.QStandardItem(f"{document.text} ({document.metadata.get('filename')})")
            model_item.setData(document, QtCore.Qt.UserRole)
            model.appendRow(QtGui.QStandardItem(model_item))
        self.listView.setModel(model)

    def selectFilesInTreeView(self, filePaths):
        selectionModel = self.treeView.selectionModel()

        # Clear previous selection
        selectionModel.clearSelection()

        for filePath in filePaths:
            index = self.model.index(filePath)
            if index.isValid():
                # This selects the item. Adjust the selection behavior as needed.
                selectionModel.select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
                # Ensure the selected item is visible
                self.treeView.scrollTo(index)
    
    def searchItemDoubleClicked(self, index):
        item = self.listView.model().itemFromIndex(index)
        document = item.data(QtCore.Qt.UserRole)
        if document:
            print("Item Double Clicked:", document)


    
    
    
            
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet("""
    #     QListView {
    #         background-color: white;
    #         border: 1px solid #d3d3d3;
    #         selection-background-color: #c3c3c3;
    #         alternate-background-color: #f0f0f0;
    #         padding: 2px;
    #     }
    #     QListView::item {
    #         margin: 2px;
    #         padding: 2px;
    #         border-radius: 2px;
    #     }
    #     QListView::item:hover {
    #         background-color: #f0f0f0;
    #     }
    #     QListView::item:selected {
    #         background-color: #a0a0a0;
    #     }
    # """)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    ui.show()
    sys.exit(app.exec_())
