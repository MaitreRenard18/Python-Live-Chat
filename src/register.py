import os
import socket

from PyQt5.QtCore import QThread, pyqtSignal


class Register(QThread):
    user_registered = pyqtSignal(str, tuple)
    
    def __init__(self, port: int = 5556):
        super().__init__()
        
        self.port = port
        self.address = "0.0.0.0"
        
        self.registry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.registry_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.registry_socket.bind((self.address, self.port))
        
    def send_username(self):
        self.registry_socket.sendto(os.environ.get("USER", "Tom").encode(), ("255.255.255.255", self.port))
    
    def run(self):
        self.send_username()
        
        while True:
            username, addr = self.registry_socket.recvfrom(256)
            self.user_registered.emit(username.decode(), addr)
            self.send_username()
    
    def close(self):
        self.registry_socket.close()
        self.quit()
