import os
import platform
import socket

from PyQt5.QtCore import QThread, pyqtSignal

BROADCAST_ADDRESS = "255.255.255.255"


class Register(QThread):
    user_registered = pyqtSignal(str, str)
    user_disconnected = pyqtSignal(str)
    
    def __init__(self, registering_port: int = 5556) -> None:
        super().__init__()
        
        self.registering_port = registering_port

        self.registry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.registry_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)      
        self.registry_socket.bind(("0.0.0.0", self.registering_port))
        
        self.username = self.get_username()
        print(f"Registered as: {self.username}")

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

    def send_username(self, discover: bool = False) -> None:
        self.registry_socket.sendto((("DISCVR " if discover else "RESPND ") + self.username).encode(), (BROADCAST_ADDRESS, self.registering_port))

    def send_disconnect(self) -> None:
        self.registry_socket.sendto(("DSCNCT " + self.username).encode(), (BROADCAST_ADDRESS, self.registering_port))

    def run(self) -> None:
        self.send_username(discover=True)
        self.user_registered.emit(self.username, self.get_ip())
        
        while True:
            data, addr = self.registry_socket.recvfrom(256)

            try:
                username = data.decode()[7:]
            except IndexError:
                print(f"Invalid username format: {data}")
                continue
            
            if username == self.username:
                continue
            
            if data.startswith(b"DSCNCT"):
                self.user_disconnected.emit(username)
                continue
            
            if data.startswith(b"DISCVR"):
                self.send_username()
            
            self.user_registered.emit(username, addr[0])
