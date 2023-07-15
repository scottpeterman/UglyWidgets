from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QApplication
import base64

class Handler(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.editor = parent

    @pyqtSlot()
    def requestPaste(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        # print(f"Pyqt: {text}")
        self.editor.page().runJavaScript(f'''replaceSelectionWithDecodedBase64(`{self.pastePlainTextAsBase64()}`);''')

    def pastePlainTextAsBase64(self):
        # Create a mime data object and set the selected text as plain text
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        text = self.encode(text)
        print(text)
        return text

    def encode(self, s):
        return base64.b64encode(s.encode()).decode()

    @pyqtSlot()
    def saveFromJs(self):
        # print(s)
        self.editor.saveFile()
        # saveFile
        # print(f"Not sure why this is called")
