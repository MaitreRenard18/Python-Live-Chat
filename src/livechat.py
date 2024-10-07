import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QEventLoop, Qt, QThread, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QFileDialog, QShortcut, QWidget

from .livechat_window import LiveChatWindow
from .popup import Popup
from .receiver import Receiver


class LiveChat(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        
        app_icon = QtGui.QIcon('assets/icon.png')
        self.setWindowIcon(app_icon)

        self.image_receiver = Receiver()
        self.image_receiver.image_received.connect(self.show_popup, Qt.QueuedConnection)
        self.image_receiver.start()
        
        self.live_chat_sender = LiveChatWindow()
        self.live_chat_sender.show()

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
