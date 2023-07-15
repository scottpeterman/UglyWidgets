from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from Library.winshellreader import ShellReaderThread
from winpty import PtyProcess
import platform

class Backend(QObject):
    send_output = pyqtSignal(str)

    def __init__(self, shell="cmd.exe", parent=None):
        super().__init__(parent)
        if platform.system() == "Windows":
            self.process = PtyProcess.spawn(shell)

        else:
            self.process = PtyProcess.spawn('bash')

        self.reader_thread = ShellReaderThread(self.process)
        self.reader_thread.data_ready.connect(self.send_output)
        self.reader_thread.start()

    @pyqtSlot(str)
    def write_data(self, data):
        if self.process.isalive():
            try:
                # print(f"Writing data to process: {data}")
                self.process.write(data)
            except Exception as e:
                print(f"Error while writing to process: {e}")

    @pyqtSlot(str)
    def set_pty_size(self, data):
        if self.process.isalive():
            try:
                cols = data.split("::")[0]
                cols = int(cols.split(":")[1])
                rows = data.split("::")[1]
                rows = int(rows.split(":")[1])
                self.process.pty.set_size(cols, rows)
                print(f"backend pty resize -> cols:{cols} rows:{rows}")
            except Exception as e:
                print(f"Error setting backend pty term size: {e}")

    def __del__(self):
        self.process.close()
