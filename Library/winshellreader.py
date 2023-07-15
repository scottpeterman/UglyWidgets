from PyQt6.QtCore import pyqtSignal, QThread


class ShellReaderThread(QThread):
    data_ready = pyqtSignal(str)

    def __init__(self, process):
        super().__init__()
        self.process = process

    def run(self):
        while True:
            if self.process.isalive():
                try:
                    # print("Reading data from process...")
                    data = self.process.read()
                    # print(f"Data: {data}")

                    self.data_ready.emit(data)
                except Exception as e:
                    print(f"Error while reading from process: {e}")
            else:
                print("not alive...")
                break
