import sys
from pathlib import Path

import PyQt5
import PyQt5.QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


class Popup(QWidget):
    def __init__(self, image_data: bytes | None = None) -> None:
        super().__init__()

        # Window settings
        self.setWindowFlag(PyQt5.QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(PyQt5.QtCore.Qt.WindowStaysOnTopHint)
        # self.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground) # TODO : uncomment this line to make the window transparent

        # Image
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        
        if image_data:
            self.set_image(image_data)

        # Resize window
        screen_size = (0, 0, PyQt5.QtWidgets.QDesktopWidget().screenGeometry().width(), PyQt5.QtWidgets.QDesktopWidget().screenGeometry().height()) 

        self.setGeometry(*screen_size)
        self.label.setGeometry(*screen_size)
        
    def set_image(self, image_data: bytes) -> None:
        image = QPixmap()
        err = image.loadFromData(image_data)
        
        if not err:
            print("Erreur lors du chargement de l'image")
            return
        
        self.label.setPixmap(image)
