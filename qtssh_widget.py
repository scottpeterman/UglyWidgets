import sys
import time
import os
import json

from PyQt6.QtCore import QSize, QCoreApplication, QUrl, QMetaObject, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebChannel import QWebChannel
from Library.sshschemahandler import WebEngineUrlSchemeHandler
from Library.sshshell import Backend

class Ui_Terminal(QWidget):
    """
    Terminal class extending QWidget to enable SSH connections in a Qt widget.
    """
    
    def __init__(self, connect_info, parent=None):
        """
        Initialization function for the Terminal class.

        :param connect_info: a dictionary that includes SSH credentials.
        :param parent: parent widget if any.
        """
        super().__init__(parent)
        self.host = connect_info.get('host')
        self.username = connect_info.get('username')
        self.password = connect_info.get('password')
        self.div_height = 0

        self.setupUi(self)

    def setupUi(self, term):
        """
        Setups UI for the terminal widget.

        :param term: terminal widget instance.
        """
        term.setObjectName("term")
        QMetaObject.connectSlotsByName(term)
        layout = QVBoxLayout()
        self.handler = WebEngineUrlSchemeHandler()
        QWebEngineProfile.defaultProfile().installUrlSchemeHandler(b"file", self.handler)
        self.channel = QWebChannel()
        self.backend = Backend(host=self.host, username=self.username, password=self.password, parrent_widget=self)
        self.channel.registerObject("backend", self.backend)

        self.view = QWebEngineView()
        self.view.page().setWebChannel(self.channel)
        self.div_height = 0
        self.webview_size = self.view.size()

        self.view.resizeEvent = self.handle_resize_event
        self.view.loadFinished.connect(self.handle_load_finished)
        self.backend.send_output.connect(lambda data: self.view.page().runJavaScript(f"window.handle_output({json.dumps(data)})"))

        self.view.load(QUrl.fromLocalFile(os.path.abspath("qtsshcon.html")))
        layout.addWidget(self.view)
        term.setLayout(layout)
        self.retranslateUi(term)

    def update_div_height(self):
        """
        Updates the div height of the terminal.
        """
        script = f"document.getElementById('terminal').style.height = '{self.div_height}px';"
        self.view.page().runJavaScript(script)

    def handle_load_finished(self):
        """
        Handles actions after the web page load has finished.
        """
        self.div_height = self.view.size().height() - 30
        self.update_div_height()
        current_size = self.view.size()
        new_size = QSize(current_size.width(), current_size.height() + 1)
        self.view.resize(new_size)
        print("loaded..")
        QTimer.singleShot(0, self.delayed_method)

    def handle_resize_event(self, event):
        """
        Handles resize events of the terminal.

        :param event: event object containing event details.
        """
        self.div_height = self.view.size().height() - 30
        if self.view.size() != self.webview_size:
            self.webview_size = self.view.size()
            self.update_div_height()

    def retranslateUi(self, term):
        """
        Retranslates the UI based on the current locale.

        :param term: terminal widget instance.
        """
        _translate = QCoreApplication.translate
        term.setWindowTitle(_translate("term", "term"))

    def delayed_method(self):
        """
        This method will be called after the web page load has finished.
        """
        print(f"Buffer: {json.dumps(self.initial_buffer)}")
        banner = json.dumps(self.initial_buffer).replace('"', '')
        self.view.page().runJavaScript(f"term.write('{banner}');")


if __name__ == "__main__":
    """
    Main function. Initializes and runs the application.
    """
    try:
        app = QApplication(sys.argv)
        mainWin = QMainWindow()
        mainWin.resize(800, 400)
        terminal = Ui_Terminal({"host":"10.0.0.12", "username": "rtruser", "password": "mypw"}, mainWin)
        mainWin.setCentralWidget(terminal)
        mainWin.setWindowTitle("PyQt6 - SSH Widget")
        mainWin.show()
        sys.exit(app.exec())

    except Exception as e:
        print(f"Exception in main: {e}")
