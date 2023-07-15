from PyQt6 import QtWidgets, QtGui, QtCore

class ImageWidget(QtWidgets.QLabel):
    def __init__(self, image_path="", parent=None):
        super().__init__(parent)

        self.setScaledContents(True)

        self.image_path = image_path
        self.set_image_file(self.image_path)

    def set_image_file(self, image_path):
        if image_path != "":
            pixmap = QtGui.QPixmap(image_path)
            self.setPixmap(pixmap)

    def set_size(self, width, height):
        self.setFixedSize(QtCore.QSize(width, height))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = ImageWidget("retro1.jpg")
    window.set_size(200, 200)
    window.show()

    sys.exit(app.exec())
