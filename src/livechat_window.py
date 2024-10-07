import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QLabel, QShortcut, QWidget

from sender import Sender


class LiveChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Live Chat")
        
        self.image_sender = Sender()
        
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.on_open)

    def on_open(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        
        if file_path:
            self.image_sender.send_image(file_path)
        else:
            print("No file selected.")
