import os
import socket


class Sender:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def send_image(self, file_path: str, address: str, port: int = 5555, duration: float | int = 5) -> None:
        if not os.path.isfile(file_path):
            print(f"{file_path} does not exist.")
            return
        
        print((address, port))
        self.client.connect((address, port))
        print(f"Sending {file_path}...")
        
        with open(file_path, "rb") as file:
            image_chunk = file.read(2048)
            
            while image_chunk:
                self.client.send(image_chunk)
                image_chunk = file.read(2048)
           
        self.client.send(b'IMAGE_END')
        self.client.send(str(duration).encode())

        print(f"Image successfully sent to {address}:{port}.")

    def close(self) -> None:
        self.client.close()
        print("Socket closed.")
