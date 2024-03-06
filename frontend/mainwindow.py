from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QStackedWidget, QTreeView, QListView, QFileDialog, QMenuBar, QMenu, QAction, QSplitter, QFileSystemModel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl
from PyQt5 import uic
import sys
from typing import List

import backend
from backend.types import Document
from backend.client import FileDBClient

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

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print("Selected file:", fileName)
            filedb.add_file(fileName)
            self.searchList()
            self.viewFile(fileName)
            
    def viewFile(self, fileName):
		# fileView stuff
        preview = QWebEngineView()
        preview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        preview.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        #filePath = QFileDialog.getOpenFileName('pdfTest.pdf')
        #url = QUrl.fromLocalFile(fileName)
        url = QUrl.fromLocalFile("pdfTest.pdf")
        print(url)
        preview.setUrl(url)
        self.graphicsView.addWidget(preview)
		

    def searchList(self):
        text = self.searchBar.text()
        # Dummy list for demonstration
        self.documents = filedb.vector_search(query_texts=[text],n_results=10)
        
        # Filter the list based on the search text
        # searched_text = [item.text for item in self.documents]

        # Update the list view
        model = DocumentStandardItemModel()
        for document in self.documents:
            model_item = QtGui.QStandardItem(document.text)
            model_item.setData(document, QtCore.Qt.UserRole)
            model.appendRow(QtGui.QStandardItem(model_item))
        self.listView.setModel(model)
    
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
