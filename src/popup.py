
import imghdr
import os
import tempfile
from enum import Enum

import PyQt5
import PyQt5.QtCore
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QLabel, QWidget


class PopupType(Enum):
    IMAGE = 1
    GIF = 2
    VIDEO = 3


class Popup(QWidget):
    def __init__(self, data: bytes, duration: float = 5.0) -> None:
        super().__init__()

        # Window settings
        self.setWindowFlag(PyQt5.QtCore.Qt.FramelessWindowHint)
        self.setWindowFlag(PyQt5.QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(PyQt5.QtCore.Qt.WA_TranslucentBackground)

        self.screen_size = (0, 0, PyQt5.QtWidgets.QDesktopWidget().screenGeometry().width(), PyQt5.QtWidgets.QDesktopWidget().screenGeometry().height()) 
        
        # Label settings
        self.label = QLabel(self)
        self.label.setScaledContents(True)

        # Media settings
        self.duration = duration
        
        self.media_path = None
        match imghdr.what("", h=data):
            case "jpeg" | "png" | "jpg":
                self.popup_type = PopupType.IMAGE
                self.set_image(data)
            
            case "gif":
                self.popup_type = PopupType.GIF
                self.set_gif(data)
                
            case _:
                raise Exception("Unsupported media type")

        # Resize window
        self.setGeometry(*self.screen_size)
        self.label.setGeometry(*self.screen_size)
    
    def set_image(self, image_data: bytes) -> None:
        image = QPixmap()
        success = image.loadFromData(image_data)
        
        if not success:
            raise Exception("Error loading image")
        
        self.label.setPixmap(image)
    
    def set_gif(self, gif_data: bytes) -> None:
        with tempfile.NamedTemporaryFile(delete=False, prefix=".gif") as gif:
            gif.write(gif_data)
            self.media_path = os.path.abspath(gif.name)
        
        q_movie = QMovie(self.media_path)
        self.label.setMovie(q_movie)
        self.duration = self.get_qmovie_duration(q_movie)
        q_movie.start()
    
    def get_qmovie_duration(self, qmovie: QMovie) -> float:
        duration = 0
        for _ in range(qmovie.frameCount()):
            duration += qmovie.nextFrameDelay()
            qmovie.jumpToNextFrame()
        
        return duration / 1000
    
    def show_popup(self) -> None:
        super().show()
        
        loop = QEventLoop()
        QTimer.singleShot(int(1000 * self.duration), loop.quit) # 1000 ms = 1s
        loop.exec()
        
        if self.popup_type == PopupType.GIF:
            self.label.setMovie(None)
        
        if self.media_path:
            os.remove(self.media_path)
        
        self.close()
