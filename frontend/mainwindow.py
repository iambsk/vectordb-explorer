from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from typing import List

import backend
from backend.types import Document

filedb = backend.fileio.FileDB(folder="../sample/sample_files",chroma_dir="../sample/chroma")


class DocumentStandardItemModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setItemData(self, index, data):
        item = self.itemFromIndex(index)
        item.setData(data, QtCore.Qt.UserRole)

class Ui_MainWindow(object):
    def __init__(self):
        self.documents: List[Document] = []
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1620, 1280)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeLabel = QtWidgets.QLabel(self.widget)
        self.treeLabel.setObjectName("treeLabel")
        self.verticalLayout_3.addWidget(self.treeLabel)
        self.treeView = QtWidgets.QTreeView(self.widget)
        self.treeView.setObjectName("treeView")
        self.verticalLayout_3.addWidget(self.treeView)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.viewLabel = QtWidgets.QLabel(self.widget1)
        self.viewLabel.setObjectName("viewLabel")
        self.verticalLayout_2.addWidget(self.viewLabel)
        self.graphicsView = QtWidgets.QGraphicsView(self.widget1)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_2.addWidget(self.graphicsView)
        self.widget2 = QtWidgets.QWidget(self.splitter)
        self.widget2.setObjectName("widget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.searchBar = QtWidgets.QLineEdit(self.widget2)
        self.searchBar.setObjectName("searchBar")
        self.verticalLayout.addWidget(self.searchBar)
        self.searchBar.returnPressed.connect(self.searchList)
        
        # INIT LIST VIEW
        
        self.listView = QtWidgets.QListView(self.widget2)   
        self.listView.setObjectName("listView")
        self.listView.doubleClicked.connect(self.searchItemDoubleClicked)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # Removes the ability to double click and edit

        self.verticalLayout.addWidget(self.listView)
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.triggered.connect(self.openFileDialog)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionNew)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Set the text and titles of the widgets in the UI
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeLabel.setText(_translate("MainWindow", "Files"))
        self.viewLabel.setText(_translate("MainWindow", "Veiw"))
        self.searchBar.setPlaceholderText(_translate("MainWindow", "Search"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
    
    
    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print("Selected file:", fileName)
            filedb.add_file(fileName)
            
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
    app.setStyleSheet("""
        QListView {
            background-color: white;
            border: 1px solid #d3d3d3;
            selection-background-color: #c3c3c3;
            alternate-background-color: #f0f0f0;
            padding: 2px;
        }
        QListView::item {
            margin: 2px;
            padding: 2px;
            border-radius: 2px;
        }
        QListView::item:hover {
            background-color: #f0f0f0;
        }
        QListView::item:selected {
            background-color: #a0a0a0;
        }
    """)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())