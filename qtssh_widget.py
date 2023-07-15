import sys
import time

from PyQt6.QtCore import QSize, QCoreApplication
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QUrl, QMetaObject, QTimer
import os
import json
from Library.sshschemahandler import WebEngineUrlSchemeHandler
from Library.sshshell import Backend

class Ui_Terminal(QWidget):
    def __init__(self, connect_info, parent=None):
        if connect_info is not None:
            self.host = connect_info['host']
            self.username = connect_info['username']
            self.password = connect_info['password']
            self.initial_buffer = ""
            # TODO: need to work on capturing prompt
            self.prompt = ""
        else:
            self.host = None
            self.username = None
            self.password = None

        super().__init__(parent)
        self.div_height = 0

        self.setupUi(self)  # call setupUi in __init__


    def setupUi(self, term):
        term.setObjectName("term")
        QMetaObject.connectSlotsByName(term)
        # Create a QVBoxLayout instance
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
        # view.show()

        # Add the QWebEngineView to the layout
        layout.addWidget(self.view)

        # Set the layout on the term
        term.setLayout(layout)
        self.retranslateUi(term)

    def update_div_height(self):
        # global div_height
        script = f"document.getElementById('terminal').style.height = '{self.div_height}px';"
        self.view.page().runJavaScript(script)

    def handle_load_finished(self):
        # global div_height
        self.div_height = self.view.size().height() - 30

        self.update_div_height()
        current_size = self.view.size()
        new_size = QSize(current_size.width(), current_size.height() + 1)
        self.view.resize(new_size)
        print("loaded..")
        QTimer.singleShot(0, self.delayed_method)

    def handle_resize_event(self, event):
        self.div_height = self.view.size().height() - 30
        if self.view.size() != self.webview_size:
            self.webview_size = self.view.size()
            self.update_div_height()



    def retranslateUi(self, term):
        _translate = QCoreApplication.translate
        term.setWindowTitle(_translate("term", "term"))
        # print(f"Intial Buffer: {self.backend.buffer}")

    def delayed_method(self):
        # This is the method that will be called after 5 seconds.

        print(f"Buffer: {json.dumps(self.initial_buffer)}")
        banner = json.dumps(self.initial_buffer).replace('"', '')
        self.view.page().runJavaScript(f"term.write('{banner}');")
        # if banner != "" and self.username not in banner:
        #     # Not picking up following prompt after banner on linux hosts
        #     self.view.page().runJavaScript(f"term.write('Connected To: {self.host}... Press Enter To Continue');")



if __name__ == "__main__":
    print("To enable chrome remote debugger add this to command line...")
    print("--webEngineArgs -remote-debugging-port=9222")
    print("http://localhost:9222")
    try:
        app = QApplication(sys.argv)

        # create a QMainWindow instance
        mainWin = QMainWindow()
        mainWin.resize(800, 400)  # resize the window to 800x800

        # create a Ui_Terminal instance


        # Linux
        terminal = Ui_Terminal({"host":"10.0.0.12", "username": "rtruser", "password": "mypw"}, mainWin)



        # set terminal as the central widget of mainWin
        mainWin.setCentralWidget(terminal)
        mainWin.setWindowTitle("PyQt6 - SSH Widget")

        mainWin.show()

        sys.exit(app.exec())

    except Exception as e:
        print(f"Exception in main: {e}")



