import socket

from PyQt5.QtCore import QThread, pyqtSignal


class Receiver(QThread):
    image_received = pyqtSignal(bytes, float)
    
    def __init__(self, address: str = "0.0.0.0", port: int = 5555) -> None:
        super().__init__()
        self.address = address
        self.port = port
        
        self.image_socket = socket.socket(type=socket.SOCK_STREAM)
        self.image_socket.bind((self.address, self.port))
        self.image_socket.listen(10)
    
    def run(self) -> None:
        while True:
            client, _ = self.image_socket.accept()
            data = b''
            
            while True:
                image_chunk = client.recv(2048)
                if b'IMAGE_END' in image_chunk:
                    parts = image_chunk.split(b'IMAGE_END')
                    data += parts[0]
                    duration = float(parts[1].decode().strip())
                    break
                else:
                    data += image_chunk

            self.image_received.emit(data, duration)
            client.close()

    def close(self) -> None:
        self.image_socket.close()
        print("Socket closed.")
