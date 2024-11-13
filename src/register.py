import os
import platform
import random
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
        
        user_id = os.environ.get("USERNAME")
        if platform.system() == "Linux":
            import pwd
            
            user_id = os.environ.get("USER")
            user_info = pwd.getpwnam(user_id)
            self.full_name = user_info.pw_gecos
        else:
            self.full_name = f"{user_id}#{str(int(random.random() * 10000)).ljust(4, '0')}"
        
        print("Registered as:", self.full_name)
        
    def send_username(self):
        self.registry_socket.sendto(self.full_name.encode(), ("255.255.255.255", self.port))
    
    def run(self):
        self.send_username()
        
        while True:
            username, addr = self.registry_socket.recvfrom(256)
            
            if username.decode() != self.full_name:
                self.user_registered.emit(username.decode(), addr)
                self.send_username()
    
    def close(self):
        self.registry_socket.close()
        self.quit()
