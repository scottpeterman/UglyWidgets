import os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QContextMenuEvent, QAction
from PyQt6.QtWidgets import QMenu, QApplication, QMessageBox, QFileDialog
from PyQt6 import QtWidgets
from PyQt6.QtCore import QUrl, QMimeData, pyqtSlot, QObject
from PyQt6.QtWebChannel import QWebChannel
import json
import base64
from Library.editor_handler import Handler

def set_status_tips_for_all_widgets(widget, tip):
    # Set the status tip for the widget
    try:
        widget.setStatusTip(tip)
    except:
        pass

    # If the widget is a container, recursively set status tips for its children
    if hasattr(widget, 'children'):
        for child in widget.children():
            try:
                set_status_tips_for_all_widgets(child, tip)
            except:
                continue

class Editor(QWebEngineView):
    def __init__(self, par, doc_text=None):
        super().__init__(par)
        self.channel = QWebChannel()
        self.handler = Handler(self)
        self.channel.registerObject('handler', self.handler)
        self.page().setWebChannel(self.channel)
        self.action = None
        self.doc_text = doc_text
        self.editor_flag = []
        self.menu_action = None
        self.file_to_open = None

        self.new_file = False
        self.parent_window = par

        # This is the local HTML path, it needs to be modified according to the actual situation.
        self.editor_index = (os.path.split(os.path.realpath(__file__))[0]) + "./ace/editor.html"
        self.loadFinished.connect(self.on_load_finished)
        self.load(QUrl.fromLocalFile(self.editor_index))

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        # Create a custom context menu
        context_menu = QMenu(self)

        # Add custom actions to the menu


        action1 = QAction("Copy", self)
        action1.triggered.connect(self.aceActionCopy)
        context_menu.addAction(action1)

        action2 = QAction("Cut", self)
        action2.triggered.connect(self.aceActionCut)
        context_menu.addAction(action2)

        action3 = QAction("Paste", self)
        action3.triggered.connect(self.aceActionPaste)
        context_menu.addAction(action3)

        action5 = QAction("Select All", self)
        action5.triggered.connect(self.aceActionSelectAll)
        context_menu.addAction(action5)

        # Show the context menu at the event's position
        context_menu.exec(self.mapToGlobal(event.pos()))

    def aceActionSelectAll(self):
        self.page().runJavaScript("editor.selectAll();")

    def aceActionCopy(self):
        self.action = "copy"
        self.page().runJavaScript("editor.getSelectedText();", self.processJavaScriptResult)

    def aceActionCut(self):
        self.action = "cut"
        self.page().runJavaScript("editor.getSelectedText();", self.processJavaScriptResult)

    def aceActionPaste(self):
        self.action = "paste"
        self.page().runJavaScript("editor.getSelectedText();", self.processJavaScriptResult)

    def saveFile(self, content):
        self.doc_text = content

    def processJavaScriptResult(self, result):
        # Handle the JavaScript result
        self.page().runJavaScript(f"console.log('{result}');")
        if self.action is not None:
            if self.action == "copy":
                print(f"copied text: {result}")
                # only did it this way due to the clipboard stuff
                self.copyPlainText(result)
                self.action = None

            if self.action == "cut":
                print(f"cut text to clipboard: {result}")
                # only did it this way due to the clipboard stuff
                self.copyPlainText(result)
                self.page().runJavaScript(f'''editor.session.replace(editor.selection.getRange(), ``);''')
                self.action = None

            elif self.action == "paste":
                print("Pasting...")
                # only did it this way due to the clipboard stuff
                self.page().runJavaScript(f'''replaceSelectionWithDecodedBase64(`{self.pastePlainTextAsBase64()}`);''')
                # self.page().runJavaScript(
                #     f'''editor.session.replace(editor.selection.getRange(), `hello from paste`);''')
                self.action = None

            elif self.action == "load":
                print("loading...")
                self.page().runJavaScript(
                    f'''replaceSelectionWithDecodedBase64(`{self.loadPlainTextAsBase64(self.doc_text)}`);''')

            elif self.action == "save":
                # file_to_save = None
                # call save file dialog
                if not self.new_file:
                    file_to_save = self.parrent_window.file_to_open
                    reply = QMessageBox.question(
                        self, f"Save File", f"Do you want to save {file_to_save}?",
                        QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Cancel
                    )

                    if reply == QMessageBox.StandardButton.Save:
                        # User clicked Save, perform save operation
                        # TODO: Implement your save logic here
                        print("Save file operation")
                        content = str(result)
                        try:
                            with open(file_to_save, "w", encoding="utf-8") as f:
                                f.write(content)
                        except Exception as e:
                            self.notify("File Error", f"Error saving file: {e}")

                    else:
                        print("Save Canceled")
                    self.action = None
                else:
                    # Never saved, ask for info
                    fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*)")
                    print(f"Saving New Content as ... {fileName}")
                    if fileName:
                        with open(fileName, "w", encoding="utf-8") as f:
                            f.write(result)
                        self.file_to_open = fileName
                        self.parent_window.file_to_open = fileName
                        self.parent_window.statusbar.showMessage(fileName)
                        return

        else:
            print("self.action not set, JavaScript result:", result)

    def copyPlainText(self, text):
        # Create a mime data object and set the selected text as plain text
        mime_data = QMimeData()
        mime_data.setText(text)
        # Set the mime data as the clipboard data
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(mime_data)

    def pastePlainText(self):
        # Create a mime data object and set the selected text as plain text
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        return text
    def pastePlainTextAsBase64(self):
        # the is the right click event
        # Create a mime data object and set the selected text as plain text
        clipboard = QApplication.clipboard()
        text = clipboard.text()

        text = self.encode(text)
        # print(text)
        return text

    def loadPlainTextAsBase64(self, text):
        text = self.encode(text)
        # print(text)
        return text

    def encode(self, s):
        return base64.b64encode(s.encode()).decode()

    def on_load_finished(self, ok):

        self.page().setWebChannel(self.channel)
        self.page().runJavaScript(f'''editor.session.setUndoManager(new ace.UndoManager());''')
        if ok:
            # Enable developer tools
            settings = self.page().settings()
            print("Ace Editor page loaded!")
            if app.file_to_open is not None:
                # backticks in source code will need to be escaped!

                if app.file_to_open.endswith(".json"):
                    mode = "json"
                elif app.file_to_open.endswith(".yaml"):
                    mode = "yaml"
                elif app.file_to_open.endswith(".sql"):
                    mode = "sql"
                elif app.file_to_open.endswith(".py"):
                    mode = "python"
                elif app.file_to_open.endswith(".js"):
                    mode = "javascript"
                elif app.file_to_open.endswith(".robot"):
                    mode = "robot"
                else:
                    mode = "text"

                self.page().runJavaScript(f'''set_mode(`{mode}`);''')

                text_to_load = self.doc_text
                self.page().runJavaScript(f"editor.setValue({text_to_load});")
                self.page().runJavaScript(f"editor.clearSelection();")
                # self.page().runJavaScript(f'''editor.session.setValue(`{text_to_load}`);''')


            # self.page().runJavaScript(f'''editor.session.on('change', function(delta) {{console.log(delta);}});''')

    def saveFile(self):
        if self.file_to_open:
            self.page().runJavaScript("editor.getValue();", self.handleSaveResult(self.file_to_open))
            self.parent_window.statusbar.showMessage(file_path)
        else:
            self.saveFileAs()

    def saveFileAs(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*)")
        if file_path:
            self.page().runJavaScript("editor.getValue();", self.handleSaveAsResult(file_path))
            self.parent_window.statusbar.showMessage(file_path)

    def notify(self, message, info):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setText(info)
        msg.setWindowTitle(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        retval = msg.exec()

    def handleSaveResult(self, file_path):
        def callback(result):
            if result:
                try:
                    with open(file_path, 'w') as file:
                        file.write(result)
                    self.parent_window.statusbar.showMessage(file_path)
                except Exception as e:
                    self.notify("Save Error", f"Error saving file: {str(e)}")

        return callback

    def handleSaveAsResult(self, file_path):
        def callback(result):
            if result:
                try:
                    with open(file_path, 'w') as file:
                        file.write(result)
                    self.file_to_open = file_path
                    self.parent_window.statusbar.showMessage(file_path)
                except Exception as e:
                    self.notify("Save Error", f"Error saving file: {str(e)}")

        return callback
class MyMenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super(MyMenuBar, self).__init__(parent)
        self.parent = parent

    def leaveEvent(self, event):
        # Mouse has left the widget, perform your actions here

        super().leaveEvent(event)
        if self.parent is not None:
            print("Mouse left the menu bar!")
            self.parent.statusbar.showMessage(self.parent.file_to_open)

    def enterEvent(self, event):
        # Mouse has left the widget, perform your actions here

        super().enterEvent(event)
        if self.parent is not None:
            print("Mouse entered the menu bar!")
            self.parent.statusbar.showMessage(self.parent.file_to_open)


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.file_to_open = None

    def setupUi(self, MainWindow, doc_text):
        self.doc_text = doc_text
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.aceBrowser = Editor(par=self.centralwidget,
                                 doc_text=self.doc_text)

        self.aceBrowser.setMinimumSize(QtCore.QSize(0, 400))
        self.aceBrowser.setObjectName("aceBrowser")
        self.aceBrowser.parent_window = self
        self.verticalLayout.addWidget(self.aceBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AceLoger = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.AceLoger.setMinimumSize(QtCore.QSize(700, 0))
        self.AceLoger.setMaximumSize(QtCore.QSize(16777215, 200))
        self.AceLoger.setObjectName("AceLoger")
        self.AceLoger.setVisible(False)

        # self.aceBrowser.page().setWebChannel(channel)
        self.horizontalLayout.addWidget(self.AceLoger)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pbAceLogger = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pbAceLogger.setObjectName("pbAceLogger")
        self.pbAceLogger.setVisible(False)
        self.horizontalLayout.addWidget(self.pbAceLogger)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar = MyMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 807, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuEdit = QtWidgets.QMenu(parent=self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuLanguage = QtWidgets.QMenu(parent=self.menubar)
        self.menuLanguage.setObjectName("menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(parent=MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.triggered.connect(lambda: self.menuFileNew())
        self.actionOpen = QtGui.QAction(parent=MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(lambda: self.menuFileOpen())
        self.actionSave = QtGui.QAction(parent=MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(lambda: self.menuSaveFile())

        self.actionSave.triggered.connect(self.aceBrowser.saveFile)
        self.actionSave_As = QtGui.QAction(parent=MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionSave_As.triggered.connect(lambda: self.menuSaveFileAs())

        self.actionExit = QtGui.QAction(parent=MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(lambda: sys.exit())
        self.actionAbout = QtGui.QAction(parent=MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPython = QtGui.QAction(parent=MainWindow)
        self.actionPython.setObjectName("actionPython")
        self.actionJavascript = QtGui.QAction(parent=MainWindow)
        self.actionJavascript.setObjectName("actionJavascript")
        self.actionRobotFramework = QtGui.QAction(parent=MainWindow)
        self.actionRobotFramework.setObjectName("actionRobotFramework")
        self.actionSQL = QtGui.QAction(parent=MainWindow)
        self.actionSQL.setObjectName("actionSQL")
        self.actionYAML = QtGui.QAction(parent=MainWindow)
        self.actionYAML.setObjectName("actionYAML")
        self.actionJSON = QtGui.QAction(parent=MainWindow)
        self.actionJSON.setObjectName("actionJSON")
        self.actionText = QtGui.QAction(parent=MainWindow)
        self.actionText.setObjectName("actionText")

        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.actionCopy = QtGui.QAction(parent=MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.menuEdit.addAction(self.actionCopy)
        # self.menuEdit.addAction(self.actionOpen)
        # self.menuEdit.addAction(self.actionSave)

        self.menuHelp.addAction(self.actionAbout)
        self.menuLanguage.addAction(self.actionPython)
        self.menuLanguage.addAction(self.actionJavascript)
        self.menuLanguage.addAction(self.actionRobotFramework)
        self.menuLanguage.addAction(self.actionSQL)
        self.menuLanguage.addAction(self.actionYAML)
        self.menuLanguage.addAction(self.actionJSON)
        self.menuLanguage.addAction(self.actionText)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.menubar.setStatusTip(self.file_to_open)
        self.statusbar.showMessage("Its All Ugly!")


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ugly Ace"))
        self.pbAceLogger.setText(_translate("MainWindow", "Log"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuLanguage.setTitle(_translate("MainWindow", "Language"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionPython.setText(_translate("MainWindow", "Python"))
        self.actionJavascript.setText(_translate("MainWindow", "Javascript"))
        self.actionRobotFramework.setText(_translate("MainWindow", "Robotframework"))
        self.actionSQL.setText(_translate("MainWindow", "SQL"))
        self.actionYAML.setText(_translate("MainWindow", "YAML"))
        self.actionJSON.setText(_translate("MainWindow", "JSON"))
        self.actionText.setText(_translate("MainWindow", "Text"))

    def menuFileNew(self):
        self.aceBrowser.page().runJavaScript("editor.setValue('');")
        self.file_to_open = None
        self.aceBrowser.new_file = True


    def menuSaveFile(self):
        if self.file_to_open is not None:
            result = self.confirm("Save File?", "Confirm File Save?")
            self.menu_action = "save"
            if result == QtWidgets.QMessageBox.StandardButton.Ok:
                print("Saving from menu")
                self.aceBrowser.menu_action = "save"
                self.menu_action = None
            else:
                print("Canceling from menu")
        else:
            self.menuSaveFileAs()

    def saveFile(self):
        if self.file_to_open is not None:
            self.saveFile()
        else:
            self.menuSaveFileAs()

    def handleEditorContentSaveAs(self, result):
        # needs to be in the handler due to async/callback nature of getting a value out of javascript
        print(result)
        try:
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*)")

            if fileName:
                print(f"Saving Content as ... {fileName}")
                with open(fileName, "w", encoding="utf-8") as f:
                    f.write(result)
                self.file_to_open = fileName

            self.statusbar.showMessage(fileName)
            self.setStatusTip(fileName)
            # self.setWindowTitle("Saved")

        except Exception as e:
            self.notify("Error Saving", f"File Save Error: {e}")


        return(result)  # or whatever you want to do with the result

    def menuSaveFileAs(self):
        # getValue returns a string, getDocument() returns an object, with a list of lines
        self.aceBrowser.page().runJavaScript(f'''editor.session.getValue();''', self.handleEditorContentSaveAs)

    def menuFileOpen(self):
        try:
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                                "All Files (*)")
            if fileName:
                with open(fileName, 'r') as file:
                    data = file.read()
                    # Load the file data into the Ace editor.
                    # Note: In order to correctly handle special characters and escape sequences,
                    # we use json.dumps to convert the file data to a JSON-compatible string.
                    content = json.dumps(data)
                    self.aceBrowser.page().runJavaScript(f"editor.setValue({content});")
                    self.aceBrowser.page().runJavaScript(f"editor.clearSelection();")
                    self.statusbar.showMessage(fileName)
                    self.file_to_open = fileName
                    self.aceBrowser.file_to_open = fileName

        except Exception as e:
            self.notify("Open Error", f"Failed to open file: {e}")

    def notify(self, message, info):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setText(info)
        msg.setWindowTitle(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        retval = msg.exec()

    def confirm(self, message, info):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msgBox.setText(info)
        msgBox.setWindowTitle(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
        returnValue = msgBox.exec()
        return returnValue


# cli python uglyeditor.py --webEngineArgs --remote-debugging-port=8011
if __name__ == "__main__":
    print(f"Debug webengine here: http://127.0.0.1:9222/")
    print("cli python uglyeditor.py --webEngineArgs --remote-debugging-port=9222")

    import sys

    cli = sys.argv
    app = QtWidgets.QApplication(sys.argv)
    active_file = None
    doc_text = ''
    if len(cli) > 1:
        file_to_open = cli[1]

        try:
            with open(file_to_open, 'r') as file:
                data = file.read()
                # Load the file data into the Ace editor.
                # Note: In order to correctly handle special characters and escape sequences,
                # we use json.dumps to convert the file data to a JSON-compatible string.
                doc_text = json.dumps(data)
                app.file_to_open = file_to_open
                active_file = app.file_to_open

        except:
            doc_text = ""
            app.file_to_open = None
    else:
        doc_text = ""
        app.file_to_open = None



    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, doc_text)
    MainWindow.show()
    if active_file is not None:
        ui.statusbar.showMessage(active_file)
        set_status_tips_for_all_widgets(ui, active_file)
        ui.file_to_open = active_file


    sys.exit(app.exec())
