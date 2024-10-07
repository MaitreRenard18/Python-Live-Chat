import os
import socket


class Sender:
    def __init__(self, address: str = "255.255.255.255", port: int = 5555):
        self.address = address
        self.port = port
        self.addr = (self.address, self.port)
        
        self.client = socket.socket(type=socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        print(f"Socket created with address {self.address} and port {self.port}.")

    def send_image(self, file_path: str, duration: float | int = 5) -> None:
        if not os.path.isfile(file_path):
            print(f"{file_path} does not exist.")
            return
        
        print(f"Sending {file_path}...")
        
        with open(file_path, "rb") as file:
            image_chunk = file.read(2048)
            
            while image_chunk:
                self.client.sendto(image_chunk, self.addr)
                image_chunk = file.read(2048)
           
        self.client.sendto(b'IMAGE_END', self.addr)
        self.client.sendto(str(duration).encode(), self.addr)

        print(f"Image successfully sent to {self.address}:{self.port}.")

    def close(self) -> None:
        self.client.close()
        print("Socket closed.")
