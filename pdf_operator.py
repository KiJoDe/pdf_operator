from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
import sys
from PyPDF2 import PdfFileMerger


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(800, 800)
        self.setWindowTitle("PDF Operator")
        self.initUI()

    model = QStandardItemModel()
    selectedDirectory = ""

    def initUI(self):
        # short infotext what the user should do to select files
        self.infotext1 = QtWidgets.QLabel(self)
        self.infotext1.setGeometry(QtCore.QRect(50, 1, 700, 50))
        self.infotext1.setObjectName("infotext1")
        self.infotext1.setText("Select your files one after another in the order they should be merged. \n" +
                               "You can delete files from the list by selecting them and clicking the delete button.")

        # creates a list widget that is used to display the files that are selected by the user after clicking on the
        # button to select the files
        self.listoffiles = QtWidgets.QListView(self)
        self.listoffiles.setGeometry(QtCore.QRect(50, 200, 700, 200))
        self.listoffiles.setObjectName("listoffiles")
        # self.listoffiles.setMovement(1)
        self.listoffiles.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        # button to select the files that should be used in the process
        self.selectFilesButton = QtWidgets.QPushButton(self)
        self.selectFilesButton.setGeometry(QtCore.QRect(150, 63, 175, 75))
        self.selectFilesButton.setObjectName("selectButton")
        self.selectFilesButton.setText("Add files")
        self.selectFilesButton.clicked.connect(self.clickedfindfiles)

        # button to remove the last added file from the list
        self.deleteLastFileButton = QtWidgets.QPushButton(self)
        self.deleteLastFileButton.setGeometry(QtCore.QRect(450, 63, 175, 75))
        self.deleteLastFileButton.setObjectName("deleteButton")
        self.deleteLastFileButton.setText("Delete the selected file \n in the list below from the list")
        self.deleteLastFileButton.clicked.connect(self.clickeddeletefiles)

        # infotext that informs that drag and drop works in the list
        self.infotext2 = QtWidgets.QLabel(self)
        self.infotext2.setGeometry(QtCore.QRect(50, 151, 700, 50))
        self.infotext2.setObjectName("infotext2")
        self.infotext2.setText("Order the files in the right order using drag and drop in the list below.")

        # infotext about the selection of a directory
        self.infotext3 = QtWidgets.QLabel(self)
        self.infotext3.setGeometry(QtCore.QRect(50, 450, 300, 50))
        self.infotext3.setObjectName("infotext3")
        self.infotext3.setText("Select the directory the new pdf should be saved in:")

        # button to select a directory
        self.selectDirectoryButton = QtWidgets.QPushButton(self)
        self.selectDirectoryButton.setGeometry(QtCore.QRect(310, 437, 175, 75))
        self.selectDirectoryButton.setObjectName("directoryButton")
        self.selectDirectoryButton.setText("Select directory")
        self.selectDirectoryButton.clicked.connect(self.clickedselectdirectory)

        # infotext that shows the selected directory
        self.selectedDirectoryText = QtWidgets.QLabel(self)
        self.selectedDirectoryText.setGeometry(QtCore.QRect(50, 525, 700, 50))
        self.selectedDirectoryText.setObjectName("selectedDirectoryText")
        self.selectedDirectoryText.setText("Selected directory: ")

        # infotext that explains the function of the field below
        self.newFileText = QtWidgets.QLabel(self)
        self.newFileText.setGeometry(QtCore.QRect(50, 575, 700, 50))
        self.newFileText.setObjectName("newFileText")
        self.newFileText.setText("Enter the file name of your new pdf:")

        # field to enter new file name
        self.newFileName = QtWidgets.QLineEdit(self)
        self.newFileName.setGeometry(QtCore.QRect(50, 615, 700, 20))
        self.newFileName.setObjectName("newFileName")

        # button to execute the merge function
        self.mergeButton = QtWidgets.QPushButton(self)
        self.mergeButton.setGeometry(QtCore.QRect(310, 675, 175, 75))
        self.mergeButton.setObjectName("mergeButton")
        self.mergeButton.setText("Merge the documents \n in the list into one pdf")
        self.mergeButton.clicked.connect(self.clickedmergefiles)

        # label that shows up when the merge was done successfully
        self.successfulMerge = QtWidgets.QLabel(self)
        self.successfulMerge.setGeometry(QtCore.QRect(50, 763, 700, 50))
        self.successfulMerge.setObjectName("successfulMergeText")
        self.successfulMerge.setAlignment(QtCore.Qt.AlignHCenter)
        self.successfulMerge.setText("")

    # method that is called when the button to select files is clicked
    # the paths to all the files are shown in the list view
    def clickedfindfiles(self):
        filenames = QFileDialog.getOpenFileNames(filter="files (*.pdf)")
        for filename in filenames[0]:
            fileitem = QStandardItem(filename)
            self.model.appendRow(fileitem)
        self.listoffiles.setModel(self.model)
        self.successfulMerge.setText("")

    def clickeddeletefiles(self):
        self.model.removeRow(self.listoffiles.selectedIndexes()[0].row())
        self.successfulMerge.setText("")

    def clickedselectdirectory(self):
        self.selectedDirectory = str(QFileDialog.getExistingDirectory())
        self.selectedDirectoryText.setText("Selected directory: " + self.selectedDirectory)
        self.successfulMerge.setText("")

    def clickedmergefiles(self):
        pdfs = []
        for row in range(self.model.rowCount()):
            pdfs.append(self.model.item(row).text())

        destination_path = self.selectedDirectory + "/" + self.newFileName.text()

        if destination_path[-4:].lower() != ".pdf":
            destination_path = destination_path + ".pdf"

        merger = PdfFileMerger()
        try:
            for pdf in pdfs:
                merger.append(open(pdf, 'rb'))
            with open(destination_path, 'wb') as fout:
                merger.write(fout)
            self.successfulMerge.setText("Finished successfully")
        except Exception as e:
            print(e)


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()
