import sys

from PyQt5.QtCore import QEventLoop, Qt, QThread, QTimer
from PyQt5.QtWidgets import QApplication, QFileDialog

from popup import Popup
from receiver import Receiver
from sender import Sender


class LiveChat(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        
        print("Thread principal: " + str(QThread.currentThreadId()))
        self.image_receiver = Receiver()
        self.image_receiver.image_received.connect(self.show_popup, Qt.QueuedConnection)
        self.image_receiver.start()
        
        self.image_sender = Sender()
        self.image_sender.open_image.connect(self.open_file, Qt.QueuedConnection)
        self.image_sender.start()

    def show_popup(self, image_data: bytes, duration: float) -> None:
        print("Affichage de la popup depuis: " + str(QThread.currentThreadId()))
        popup = Popup(image_data)
        popup.show()
        
        loop = QEventLoop()
        QTimer.singleShot(int(1000 * duration), loop.quit) # 1000 ms = 1s
        loop.exec()
        
        popup.hide()
        
    def open_file(self) -> None:
        print("Ouverture de l'explorateur de fichier depuis: " + str(QThread.currentThreadId()))
        image_path = QFileDialog.getOpenFileName()[0]
        self.image_sender.send_image(image_path)


if __name__ == "__main__":
    app = LiveChat()
    app.exec()
