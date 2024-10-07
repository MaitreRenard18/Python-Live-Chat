from pathlib import Path

import PyQt5
import PyQt5.QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


class Popup(QWidget):
    def __init__(self, image_data: bytes) -> None:
        super().__init__()

        # Window settings
        self.setWindowFlag(PyQt5.QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(PyQt5.QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)

        # Image
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        
        image = QPixmap()
        err = image.loadFromData(image_data)
        
        if not err:
            print("Error loading image.")
        
        self.label.setPixmap(image)

        # Resize window
        screen_size = (0, 0, PyQt5.QtWidgets.QDesktopWidget().screenGeometry().width(), PyQt5.QtWidgets.QDesktopWidget().screenGeometry().height()) 

        self.setGeometry(*screen_size)
        self.label.setGeometry(*screen_size)
