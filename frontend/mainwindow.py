from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QStackedWidget, QTreeView, QListView, QFileDialog, QMenuBar, QMenu, QAction, QSplitter, QFileSystemModel, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, QMimeData, Qt
from PyQt5 import uic
import pathlib
from typing import List
import qdarkgraystyle

import backend
from backend.types import Document
from backend.client import FileDBClient
from pathlib import Path

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

        #Drag and Drop support
        self.setAcceptDrops(True)
        
        # self.label = QLabel("Drag and Drop Files Here")
        # self.layout.addWidget(self.label)
        # self.setlayout(self.layout)

        # load the ui file
        uic.loadUi("mainwindow.ui", self)

        # defs from ui file
        self.searchBar = self.findChild(QLineEdit , "searchBar")
        self.graphicsView = self.findChild(QStackedWidget, "stackedWidget")
        self.treeView = self.findChild(QTreeView, "treeView")
        self.listView = self.findChild(QListView, "listView")
        self.setStyleSheet("selection-background-color: transparent")
        self.listView.doubleClicked.connect(self.searchItemDoubleClicked)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # Removes the ability to double click and edit
        self.treeView.hideColumn(1)  # Example: Hide the size column
        self.treeView.hideColumn(2)  # Hide the type column
        self.treeView.hideColumn(3)  # Hide the date modified column
        
        # Adding file system tree view
        self.model = QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.rootPath())  # Or any specific path you want to show

        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(filedb.folder))  # Adjust if you're using a specific path      
        # Optional: Customize the view
        self.treeView.hideColumn(1)  # Example: Hide the size column
        self.treeView.hideColumn(2)  # Hide the type column
        self.treeView.hideColumn(3)  #          Hide the date modified column
        
        
        self.splitter = self.findChild(QSplitter, "splitter")       
        self.menubar = self.findChild(QMenuBar, "menubar")
        self.menuFile = self.findChild(QMenu, "menuFile")
        self.menuPreferences = self.findChild(QMenu, "menuPreferences")
        self.actionNew = self.findChild(QAction, "actionNew")
        self.menuView = self.findChild(QMenu, "menuView")
        
        self.actionChange_Directory = self.findChild(QAction, "actionChange_Directory")
        self.actionChroma_Dir = self.findChild(QAction, "actionChroma_Dir")
        
        self.actionChange_Directory.triggered.connect(self.changeDirectory)
        self.actionChroma_Dir.triggered.connect(self.changeChromaDirectory)

        # connect
        self.splitter.setSizes([50, 100, 50])
        self.searchBar.setPlaceholderText("Search")
        self.searchBar.returnPressed.connect(self.searchList)
        self.actionNew.triggered.connect(self.openFileDialog)
        
        
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openContextMenu)
        self.treeView.selectionModel().currentChanged.connect(self.viewFile)

        folderIndex = self.model.index(filedb.folder)
        self.treeView.expand(folderIndex)

        self.treeView.scrollTo(folderIndex, QTreeView.EnsureVisible)
    
    def viewFile(self):
        cWidget = self.graphicsView.currentWidget()
        self.graphicsView.removeWidget(cWidget)
        preview = QWebEngineView()
        preview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        preview.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        index = self.treeView.currentIndex()
        info = self.treeView.model().fileInfo(index)
        filePath = info.absoluteFilePath()
        fileExtension = pathlib.Path(filePath).suffix
        if fileExtension in ['.pdf', '.txt', '.html']:
            url = QUrl.fromLocalFile(filePath)
            print(url)
            preview.setUrl(url)
            self.graphicsView.addWidget(preview)
            
    def selectFilesInTreeView(self, filePaths):
        selectionModel = self.treeView.selectionModel()

        # Clear previous selection
        selectionModel.clearSelection()

        # Define the selection flag to select and highlight the row
        selectionFlag = QItemSelectionModel.Select | QItemSelectionModel.Rows

        for filePath in filePaths:
            index = self.model.index(filePath)
            if index.isValid():
                # This selects the item. Adjust the selection behavior as needed.
                selectionModel.select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
                # Ensure the selected item is visible
                self.treeView.scrollTo(index)
                
    def openContextMenu(self, position):
        contextMenu = QMenu(self)
        deleteAction = contextMenu.addAction("Delete File")
        action = contextMenu.exec_(self.treeView.viewport().mapToGlobal(position))
        if action == deleteAction:
            self.deleteSelectedFiles()
            
    def refreshView(self):
        self.searchList()
    
    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print("Selected file:", fileName)
            filedb.add_file(fileName)
            self.searchList()
    
    def changeDirectory(self):
        # Open dialog to select a directory for the main file database
        path = Path(filedb.folder)
        folder = QFileDialog.getExistingDirectory(self, "Select Directory", str(path.parent.absolute()))
        if folder:
            print("Selected directory:", folder)
            # Update the vectordb folder
            filedb.update_folder(folder)
            self.refreshView() 
    def changeChromaDirectory(self):
        # Open dialog to select a directory for the chroma files
        path = Path(filedb.chroma_dir)
        chroma_dir = QFileDialog.getExistingDirectory(self, "Select Chroma Directory", str(path.parent.absolute()))
        if chroma_dir:
            print("Selected chroma directory:", chroma_dir)
            # Update the chroma directory location
            filedb.update_chroma_dir(chroma_dir)
            self.refreshView() 
            
    def searchList(self):
        text = self.searchBar.text()
        # Dummy list for demonstration
        self.documents = filedb.vector_search(query_texts=[text],n_results=10)
        
        # Filter the list based on the search text
        # searched_text = [item.text for item in self.documents]

        # Update the list view
        model = DocumentStandardItemModel()
        for document in self.documents:
            model_item = QtGui.QStandardItem(f"{document.text} \n({document.metadata.get('filename')})")
            model_item.setData(document, QtCore.Qt.UserRole)
            model.appendRow(QtGui.QStandardItem(model_item))
        self.listView.setModel(model)
        self.selectFilesInTreeView([doc.metadata['filename'] for doc in self.documents])
    
    def searchItemDoubleClicked(self, index):
        item = self.listView.model().itemFromIndex(index)
        document = item.data(QtCore.Qt.UserRole)
        if document:
            print("Item Double Clicked:", document)
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
                    filedb.delete_file(file_path)
                    # Optionally, refresh the QFileSystemModel or parent directory to reflect the deletion
                    self.model.removeRow(index.row(), index.parent())
                    self.refreshView()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                filepath = url.toLocalFile()
                if pathlib.Path(filepath).is_file():
                    event.accept()
                    return
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                filepath = url.toLocalFile()
                if pathlib.Path(filepath).is_file():
                    print("Dropped file:", filepath)
                    filedb.add_file(filepath)
                    self.searchList()
        else:
            event.ignore()
        

    
    
    
            
            
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
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    MainWindow = QtWidgets.QMainWindow()
    ui = UI()
    
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    ui.show()
    sys.exit(app.exec_())
