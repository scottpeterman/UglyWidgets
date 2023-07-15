from PyQt6.QtCore import pyqtSignal, QThread


class ShellReaderThread(QThread):
    data_ready = pyqtSignal(str)

    def __init__(self, channel, buffer, parent_widget):
        super().__init__()
        self.channel = channel
        self.intial_buffer = buffer
        self.parrent_widget = parent_widget

    def run(self):
        while True:
            if not self.channel.closed:
                try:
                    data = self.channel.recv(1024)

                    if data:
                        # for debugging
                        if self.intial_buffer == "":
                            self.intial_buffer = bytes(data).decode('utf-8')
                            # print(bytes(data).decode('utf-8'))
                            # self.parrent_widget.view.page().runJavaScript(f"window.handle_output({bytes(data).decode('utf-8')}")
                            self.parrent_widget.initial_buffer = bytes(data).decode('utf-8')

                        self.data_ready.emit(data.decode())
                except Exception as e:
                    print(f"Error while reading from channel: {e}")
            else:
                print("Channel closed...")
                break
