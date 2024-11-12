import socket
from random import randint

from PyQt5.QtCore import QThread, pyqtSignal


class Receiver(QThread):
    image_received = pyqtSignal(bytes, float)
    
    def __init__(self, address: str = "0.0.0.0", port: int = 5555):
        super().__init__()

        self.address = address
        self.port = port
        
        self.image_socket = socket.socket(type=socket.SOCK_STREAM)
        self.image_socket.bind((self.address, self.port))
        self.image_socket.listen(1)
    
    def run(self) -> None:
        while True:
            client, _ = self.image_socket.accept()
            data = b''
            
            image_chunk = client.recv(2048)
            while image_chunk and image_chunk != b'IMAGE_END':
                data += image_chunk
                image_chunk = client.recv(2048)

            print("Image received.")

            duration = float(client.recv(2048).decode())
            self.image_received.emit(data, duration)
            
            client.close()

    def close(self) -> None:
        self.image_socket.close()
        print("Socket closed.")
