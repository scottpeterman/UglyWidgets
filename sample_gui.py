from PyQt6 import QtCore, QtGui, QtWidgets
from qtexplorer_widget import FileTree
from qtace_widget import QtAceWidget
from qtssh_widget import Ui_Terminal as SSH
from qtwincon_widget import Ui_Terminal as Wincon
from qtimage_widget import ImageWidget
class Ui_NESTMainWindow(object):
    def setupUi(self, NESTMainWindow):
        NESTMainWindow.setObjectName("NESTMainWindow")
        NESTMainWindow.resize(1297, 865)
        self.centralwidget = QtWidgets.QWidget(parent=NESTMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(parent=self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(parent=self.splitter)
        self.widget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.FileExplorer = FileTree()
        self.FileExplorer.setObjectName("FileExplorer")
        self.verticalLayout_2.addWidget(self.FileExplorer)
        self.widget_2 = QtWidgets.QWidget(parent=self.splitter)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter_2 = QtWidgets.QSplitter(parent=self.widget_2)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.widget_3 = QtWidgets.QWidget(parent=self.splitter_2)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.splitter_3 = QtWidgets.QSplitter(parent=self.widget_3)
        self.splitter_3.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.widget_5 = QtWidgets.QWidget(parent=self.splitter_3)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        # self.SSH = QtWidgets.QTextEdit(parent=self.widget_5)

        self.SSH = SSH({"host": "10.0.0.12", "username": "linux_user", "password": "mypw"},
                       self.widget_5)
        self.SSH.setObjectName("SSH")
        self.verticalLayout_6.addWidget(self.SSH)
        self.widget_6 = QtWidgets.QWidget(parent=self.splitter_3)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.Terminal = Wincon()
        self.Terminal.setObjectName("Terminal")
        self.verticalLayout_7.addWidget(self.Terminal)
        self.verticalLayout_4.addWidget(self.splitter_3)
        self.widget_4 = QtWidgets.QWidget(parent=self.splitter_2)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.splitter_4 = QtWidgets.QSplitter(parent=self.widget_4)
        self.splitter_4.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.widget_7 = QtWidgets.QWidget(parent=self.splitter_4)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        
        self.Ace = QtAceWidget(parent=self.widget_7)
        self.Ace.setObjectName("Ace")
        self.verticalLayout_9.addWidget(self.Ace)
        self.widget_8 = QtWidgets.QWidget(parent=self.splitter_4)
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_8)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        
        self.Browser = ImageWidget()
        self.Browser.set_image_file("sample_map.jpg")
        # self.Browser.set_image_file("sample_map.png")
        self.Browser.set_size(400, 200)
        self.Browser.setObjectName("Browser")
        self.verticalLayout_8.addWidget(self.Browser)
        self.verticalLayout_5.addWidget(self.splitter_4)
        self.verticalLayout_3.addWidget(self.splitter_2)
        self.verticalLayout.addWidget(self.splitter)
        NESTMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=NESTMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1297, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(parent=self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuSSH = QtWidgets.QMenu(parent=self.menubar)
        self.menuSSH.setObjectName("menuSSH")
        self.menuTools = QtWidgets.QMenu(parent=self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuOptions = QtWidgets.QMenu(parent=self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        NESTMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=NESTMainWindow)
        self.statusbar.setObjectName("statusbar")
        NESTMainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(parent=NESTMainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionPaste = QtGui.QAction(parent=NESTMainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionNew_Connection = QtGui.QAction(parent=NESTMainWindow)
        self.actionNew_Connection.setObjectName("actionNew_Connection")
        self.actionParsers = QtGui.QAction(parent=NESTMainWindow)
        self.actionParsers.setObjectName("actionParsers")
        self.actionSettings = QtGui.QAction(parent=NESTMainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSSH = QtGui.QAction(parent=NESTMainWindow)
        self.actionSSH.setObjectName("actionSSH")
        self.actionEditor = QtGui.QAction(parent=NESTMainWindow)
        self.actionEditor.setObjectName("actionEditor")
        self.actionTerminal = QtGui.QAction(parent=NESTMainWindow)
        self.actionTerminal.setObjectName("actionTerminal")
        self.actionAbout = QtGui.QAction(parent=NESTMainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionOpen)
        self.menuEdit.addAction(self.actionPaste)
        self.menuSSH.addAction(self.actionNew_Connection)
        self.menuTools.addAction(self.actionParsers)
        self.menuOptions.addAction(self.actionSettings)
        self.menuView.addAction(self.actionSSH)
        self.menuView.addAction(self.actionEditor)
        self.menuView.addAction(self.actionTerminal)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSSH.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(NESTMainWindow)
        QtCore.QMetaObject.connectSlotsByName(NESTMainWindow)

    def retranslateUi(self, NESTMainWindow):
        _translate = QtCore.QCoreApplication.translate
        NESTMainWindow.setWindowTitle(_translate("NESTMainWindow", "NEST - Its All Ugly"))
        self.menuFile.setTitle(_translate("NESTMainWindow", "File"))
        self.menuEdit.setTitle(_translate("NESTMainWindow", "Edit"))
        self.menuSSH.setTitle(_translate("NESTMainWindow", "SSH"))
        self.menuTools.setTitle(_translate("NESTMainWindow", "Tools"))
        self.menuOptions.setTitle(_translate("NESTMainWindow", "Options"))
        self.menuView.setTitle(_translate("NESTMainWindow", "View"))
        self.menuHelp.setTitle(_translate("NESTMainWindow", "Help"))
        self.actionOpen.setText(_translate("NESTMainWindow", "Open"))
        self.actionPaste.setText(_translate("NESTMainWindow", "Paste"))
        self.actionNew_Connection.setText(_translate("NESTMainWindow", "New Connection"))
        self.actionParsers.setText(_translate("NESTMainWindow", "Parsers"))
        self.actionSettings.setText(_translate("NESTMainWindow", "Settings"))
        self.actionSSH.setText(_translate("NESTMainWindow", "SSH"))
        self.actionEditor.setText(_translate("NESTMainWindow", "Editor"))
        self.actionTerminal.setText(_translate("NESTMainWindow", "Terminal"))
        self.actionAbout.setText(_translate("NESTMainWindow", "About"))


if __name__ == "__main__":
    import sys
    from qt_material import apply_stylesheet

    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_lightgreen.xml')
    NESTMainWindow = QtWidgets.QMainWindow()
    ui = Ui_NESTMainWindow()
    ui.setupUi(NESTMainWindow)
    NESTMainWindow.show()
    sys.exit(app.exec())

# Themes from qt_material   https://pypi.org/project/qt-material/
# "amber": "dark_amber.xml",
# "dark lg": "dark_lightgreen.xml",
# "dark cyan": "dark_cyan.xml",
# "dark blue": "dark_blue.xml",
