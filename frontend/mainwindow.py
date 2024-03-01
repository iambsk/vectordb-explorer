# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
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
        self.searchBar.textChanged.connect(self.searchList)
        
        # INIT LIST VIEW
        
        self.listView = QtWidgets.QListView(self.widget2)   
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        file_list = ["/home/user/file1.txt", "/home/user/file2.txt", "/home/user/file3.txt", "/home/user/file4.txt", "/home/user/file5.txt", "/home/user/file6.txt", "/home/user/file7.txt", "/home/user/file8.txt", "/home/user/file9.txt", "/home/user/file10.txt"]
        model = QtGui.QStandardItemModel()
        for item in file_list:
            model.appendRow(QtGui.QStandardItem(item))
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
            
    def searchList(self, text):
        # Dummy list for demonstration
        file_list = ["/home/user/file1.txt", "/home/user/file2.txt", "/home/user/file3.txt", "/home/user/file4.txt", "/home/user/file5.txt", "/home/user/file6.txt", "/home/user/file7.txt", "/home/user/file8.txt", "/home/user/file9.txt", "/home/user/file10.txt"]
        
        # Filter the list based on the search text
        filtered_list = [item for item in file_list if text.lower() in item.lower()]

        # Update the list view
        model = QtGui.QStandardItemModel()
        for item in filtered_list:
            model.appendRow(QtGui.QStandardItem(item))
        self.listView.setModel(model)
            
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())