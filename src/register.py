import os
import platform
import socket

from PyQt5.QtCore import QThread, pyqtSignal


class Register(QThread):
    user_registered = pyqtSignal(str, tuple)
    user_disconnected = pyqtSignal(str)
    
    def __init__(self, port: int = 5556):
        super().__init__()
        
        self.port = port
        self.address = "0.0.0.0"
        
        self.registry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.registry_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)      
        self.registry_socket.bind((self.address, self.port))
        
        if platform.system() == "Linux":
            import pwd
            
            user_id = os.environ.get("USER")
            self.full_name = pwd.getpwnam(user_id).pw_gecos
        else:
            self.full_name = os.environ.get("USERNAME")
        
        self.full_name += ":" + socket.gethostbyname(socket.gethostname())
        print(f"Registered as: {self.full_name}")

    def send_username(self, discover: bool = False):
        self.registry_socket.sendto((("DISCVR " if discover else "RESPND ") + self.full_name).encode(), ("255.255.255.255", self.port))

    def send_disconnect(self):
        self.registry_socket.sendto(("DSCNCT " + self.full_name).encode(), ("255.255.255.255", self.port))

    def run(self):
        self.send_username(discover=True)
        self.user_registered.emit(self.full_name, (socket.gethostbyname(socket.gethostname()), 5555)) # TODO Use actual port
        
        while True:
            data, addr = self.registry_socket.recvfrom(256)

            try:
                username = data.decode()[7:]
            except IndexError:
                print(f"Invalid username format: {data}")
                continue
            
            if username == self.full_name:
                continue
            
            if data.startswith(b"DSCNCT"):
                self.user_disconnected.emit(username)
                continue
            
            if data.startswith(b"DISCVR"):
                self.send_username()
            
            self.user_registered.emit(username, addr)
