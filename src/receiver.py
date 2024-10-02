import socket
import sys
from threading import Thread
from time import sleep

from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication

from popup import Popup

_popup: Popup = None


def receive(port: int = 5555) -> None:
    addr = ("0.0.0.0", port)

    server = socket.socket(type=socket.SOCK_DGRAM)
    server.bind(addr)

    print("En attente d'image")
    while ...:
        image_chunk, _addr = server.recvfrom(2048)

        if not image_chunk:
            continue

        print("Debut du téléchargement de l'image...")

        data = b""
        while image_chunk and image_chunk != b'END':
            data += image_chunk
            image_chunk = server.recv(2048)

        print("Téléchargement de l'image fini.")

        # Affiche le popup
        _popup.set_image(data)
        _popup.show()

    server.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    _popup = Popup()
    
    receive_thread = Thread(target=receive)
    receive_thread.start()
    
    app.exec()
