import sys

from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtWidgets import QApplication

from popup import Popup
from receiver import Receiver


class ReceiverApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        
        self.popup = Popup()
        
        self.receiver = Receiver()
        self.receiver.image_received.connect(self.show_popup)
        self.receiver.start()

    def show_popup(self, image_data: bytes, duration: float) -> None:
        print("Affichage de la popup...")
        self.popup.set_image(image_data)
        self.popup.show()
        
        loop = QEventLoop()
        QTimer.singleShot(int(1000 * duration), loop.quit) # 1000 ms = 1s
        loop.exec()
        
        self.popup.hide()


if __name__ == "__main__":
    app = ReceiverApp()
    app.exec()
