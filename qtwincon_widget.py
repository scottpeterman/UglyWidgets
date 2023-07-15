import sys
from PyQt6.QtCore import QSize, QCoreApplication
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QUrl ,QMetaObject
import os
import json
from Library.winschemahandler import WebEngineUrlSchemeHandler
from Library.winshell import Backend

class Ui_Terminal(QWidget):
    def __init__(self, shell="cmd.exe", parent=None):
        super().__init__(parent)
        self.div_height = 0
        self.shell = shell
        self.setupUi(self)  # call setupUi in __init__

        # print("initialized?")

    def setupUi(self, term):
        term.setObjectName("term")
        QMetaObject.connectSlotsByName(term)

        self.handler = WebEngineUrlSchemeHandler()
        # default
        QWebEngineProfile.defaultProfile().installUrlSchemeHandler(b"file", self.handler)
        self.channel = QWebChannel()
        self.backend = Backend(self.shell)
        self.channel.registerObject("backend", self.backend)

        # Create a QVBoxLayout instance
        layout = QVBoxLayout()

        self.view = QWebEngineView()
        self.view.page().setWebChannel(self.channel)
        self.webview_size = self.view.size()
        self.view.resizeEvent = self.handle_resize_event
        self.view.loadFinished.connect(self.handle_load_finished)

        self.backend.send_output.connect(lambda data: self.view.page().runJavaScript(f"window.handle_output({json.dumps(data)})"))
        self.view.load(QUrl.fromLocalFile(os.path.abspath("qtwincon.html")))

        # Add the QWebEngineView to the layout
        layout.addWidget(self.view)

        # Set the layout on the term
        term.setLayout(layout)

        self.retranslateUi(term)

    def update_div_height(self):
        script = f"document.getElementById('terminal').style.height = '{self.div_height}px';"
        self.view.page().runJavaScript(script)

    def handle_load_finished(self):
        # global div_height
        self.div_height = self.view.size().height() - 30

        self.update_div_height()
        current_size = self.view.size()
        new_size = QSize(current_size.width(), current_size.height() - 1)
        self.view.resize(new_size)

    def handle_resize_event(self, event):
        # nonlocal webview_size
        # global div_height
        self.div_height = self.view.size().height() - 30
        if self.view.size() != self.webview_size:
            self.webview_size = self.view.size()
            self.update_div_height()

    def retranslateUi(self, term):
        _translate = QCoreApplication.translate
        term.setWindowTitle(_translate("term", "term"))

def main():
    try:
        app = QApplication(sys.argv)

        # create a QMainWindow instance
        mainWin = QMainWindow()
        mainWin.resize(800, 400)  # resize the window to 800x800

        # create a Ui_Terminal instance
        shell = "cmd.exe"
        # shell = "powershell.exe"
        # shell = "wsl.exe"
        terminal = Ui_Terminal(shell, mainWin)

        # set terminal as the central widget of mainWin
        mainWin.setCentralWidget(terminal)

        mainWin.show()
        mainWin.setWindowTitle(f"PyQt6 - Terminal Widget - Shell is: {shell}")
        sys.exit(app.exec())

    except Exception as e:
        print(f"Exception in main: {e}")


if __name__ == "__main__":
    print("To enable chrome remote debugger add this to command line...")
    print("--webEngineArgs -remote-debugging-port=9222")
    print("http://localhost:9222")
    main()
