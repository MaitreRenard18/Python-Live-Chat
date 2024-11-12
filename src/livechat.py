import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QEventLoop, Qt, QThread, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QFileDialog, QShortcut, QWidget

from .livechat_window import LiveChatWindow
from .popup import Popup
from .receiver import Receiver
from .register import Register
from .sender import Sender


class LiveChat(QApplication):
    def __init__(self, show_sender=True):
        super().__init__(sys.argv)
        
        # App settings
        app_icon = QtGui.QIcon('assets/icon.png')
        self.setWindowIcon(app_icon)

        # Receiver
        self.image_receiver = Receiver()
        self.image_receiver.image_received.connect(self.show_popup, Qt.QueuedConnection)
        self.image_receiver.start()
        
        # Registry
        self.registry = {}
        
        self.user_register = Register()
        self.user_register.user_registered.connect(self.register_user, Qt.QueuedConnection)
        self.user_register.start()
        
        # Sender
        if show_sender:
            self.live_chat_sender = LiveChatWindow()
            self.live_chat_sender.show()

            self.image_sender = Sender()
            self.live_chat_sender.send_image.connect(self.send_image, Qt.QueuedConnection)
    
    def send_image(self, image_path: str, duration: int = 5) -> None:
        for address in self.registry.keys():
            self.image_sender.send_image(image_path, address=address, duration=duration)
    
    def register_user(self, username: str, address: tuple[str, int]) -> None:
        self.registry[username] = address
    
    def show_popup(self, image_data: bytes, duration: float) -> None:
        popup = Popup(image_data)
        popup.show()
        
        loop = QEventLoop()
        QTimer.singleShot(int(1000 * duration), loop.quit) # 1000 ms = 1s
        loop.exec()
        
        popup.hide()


if __name__ == "__main__":
    app = LiveChat()
    app.exec()
