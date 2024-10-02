import socket

from PyQt5.QtCore import QThread, pyqtSignal


class Receiver(QThread):
    image_received = pyqtSignal(bytes)  # Ensure this is 'bytes'

    def __init__(self, port: int = 5555) -> None:
        super().__init__()

        self.addr = ("0.0.0.0", port)
        self.server = socket.socket(type=socket.SOCK_DGRAM)
        self.server.bind(self.addr)

    def run(self) -> None:
        print("En attente d'image")
        while True:  # Replace ... with True to keep running
            image_chunk, _addr = self.server.recvfrom(2048)

            if not image_chunk:
                continue

            print("Debut du téléchargement de l'image...")

            data = b""
            while image_chunk and image_chunk != b'END':
                data += image_chunk
                image_chunk = self.server.recv(2048)

            print("Téléchargement de l'image fini.")

            self.image_received.emit(data)  # Emit the bytes data
