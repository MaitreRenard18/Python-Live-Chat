import os
import platform
import socket

from PyQt5.QtCore import QThread, pyqtSignal


class Register(QThread):
    user_registered = pyqtSignal(str, str)
    user_disconnected = pyqtSignal(str)
    
    def __init__(self, registering_port: int = 5556):
        super().__init__()
        
        self.registering_port = registering_port
        self.address = "0.0.0.0"
        
        self.registry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.registry_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)      
        self.registry_socket.bind((self.address, self.registering_port))
        
        self.full_name = self.get_username()
        print(f"Registered as: {self.full_name}")

    def get_ip(self) -> str:
        return socket.gethostbyname(socket.gethostname())
    
    def get_username(self) -> str:
        if platform.system() == "Linux":
            import pwd
            
            user_id = os.environ.get("USER")
            full_name = pwd.getpwnam(user_id).pw_gecos
        else:
            full_name = os.environ.get("USERNAME")
        
        return full_name + " " + str(self.get_ip())

    def send_username(self, discover: bool = False):
        self.registry_socket.sendto((("DISCVR " if discover else "RESPND ") + self.full_name).encode(), ("255.255.255.255", self.registering_port))

    def send_disconnect(self):
        self.registry_socket.sendto(("DSCNCT " + self.full_name).encode(), ("255.255.255.255", self.registering_port))

    def run(self):
        self.send_username(discover=True)
        self.user_registered.emit(self.full_name, self.get_ip())
        
        while True:
            data, addr = self.registry_socket.recvfrom(256)

            print(data)

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
            
            self.user_registered.emit(username, addr[0])
