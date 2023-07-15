import os
import base64
from PyQt6 import QtWidgets, QtWebEngineWidgets
from PyQt6.QtGui import QContextMenuEvent, QAction
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QUrl, QMimeData, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel

from Library.editor_handler import Handler

class Editor(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, par, doc_text=None):
        super().__init__(par)
        self.channel = QWebChannel()
        self.handler = Handler(self)
        self.channel.registerObject('handler', self.handler)
        self.page().setWebChannel(self.channel)
        self.action = None
        self.doc_text = doc_text
        self.parrent_window = par
        self.new_file = False

        # Load the HTML file for the editor
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ace_html = current_dir.split("Library")[0] + "ace/editor.html"

        self.load(QUrl.fromLocalFile(ace_html))

        # Connect loadFinished signal to initializeEditor slot
        self.loadFinished.connect(self.initializeEditor)

    def initializeEditor(self, ok):
        if ok:
            # Enable developer tools
            settings = self.page().settings()
            #settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.WebAttribute.DeveloperExtrasEnabled, True)
            # Set up the web channel
            self.page().setWebChannel(self.channel)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        # Create a custom context menu
        context_menu = QtWidgets.QMenu(self)

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
        # Perform the save operation
        # You can implement your own logic here to save the content to a file or database

    def loadFile(self, file_path):
        self.action = "load"
        self.parrent_window.file_to_open = file_path
        with open(file_path, 'r') as file:
            content = file.read()
            self.doc_text = content
            self.page().runJavaScript(f"editor.setValue(``);")
            self.page().runJavaScript("replaceSelectionWithDecodedBase64", self.processJavaScriptResult)


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
                self.page().runJavaScript(f'''replaceSelectionWithDecodedBase64(`{self.loadPlainTextAsBase64(self.doc_text)}`);''')

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
                        self.parrent_window.file_to_open = fileName
                        self.parrent_window.statusbar.showMessage(fileName)
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

