import imghdr
import os
import tempfile

import PyQt5
import PyQt5.QtCore
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget


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

        self.gif_path = None
        self.is_gif = imghdr.what("", h=image_data) == "gif"
        if self.is_gif:
            self.show_gif(image_data)
        else:
            self.show_image(image_data)

        # Resize window
        screen_size = (0, 0, PyQt5.QtWidgets.QDesktopWidget().screenGeometry().width(), PyQt5.QtWidgets.QDesktopWidget().screenGeometry().height()) 

        self.setGeometry(*screen_size)
        self.label.setGeometry(*screen_size)

    def show_image(self, image_data: bytes) -> None:
        image = QPixmap()
        success = image.loadFromData(image_data)
        
        if not success:
            raise Exception("Error loading image")
        
        self.label.setPixmap(image)
    
    def get_qmovie_duration(self, qmovie: QMovie) -> float:
        duration = 0
        for _ in range(qmovie.frameCount()):
            duration += qmovie.nextFrameDelay()
            qmovie.jumpToNextFrame()
        
        return duration / 1000
    
    def show_gif(self, gif_data: bytes) -> None:
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as gif:
            gif.write(gif_data)
            self.gif_path = os.path.abspath(gif.name)
        
        q_movie = QMovie(self.gif_path)
        self.label.setMovie(q_movie)
        q_movie.start()

    def show(self, duration: float = 5) -> None:
        super().show()
        
        if self.is_gif:
            duration = self.get_qmovie_duration(self.label.movie())
        
        loop = QEventLoop()
        QTimer.singleShot(int(1000 * duration), loop.quit) # 1000 ms = 1s
        loop.exec()
        
        if self.is_gif:
            self.label.setMovie(None)
            os.remove(self.gif_path) if self.is_gif else None
        
        self.close()
