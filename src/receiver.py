import socket
from random import randint

from PyQt5.QtCore import QThread, pyqtSignal


class Receiver(QThread):
    image_received = pyqtSignal(bytes, float)
    
    def __init__(self, address: str = "0.0.0.0", port: int = 5555):
        super().__init__()

        self.address = address
        self.port = port
        self.addr = (self.address, self.port)
        
        self.server = socket.socket(type=socket.SOCK_DGRAM)
        self.server.bind(self.addr)
        
        print(f"Socket created with address {self.address} and port {self.port}.")
    
    def run(self) -> None:
        while True:
            image_chunk, current_addr = self.server.recvfrom(2048)

            if not image_chunk:
                continue

            data = b""
            while image_chunk and image_chunk != b'IMAGE_END':
                data += image_chunk
                new_image_chunk, addr = self.server.recvfrom(2048)
                
                if addr == current_addr:
                    image_chunk = new_image_chunk

            print("Téléchargement de l'image fini.")

            duration = float(self.server.recv(2048).decode())
            self.image_received.emit(data, duration)

    def close(self) -> None:
        self.server.close()
        print("Socket closed.")
