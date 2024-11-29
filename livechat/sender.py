import os
import socket


class Sender:
    def send_image(self, file_path: str, address: str, port: int = 5555, duration: float | int = 5) -> None:
        if not os.path.isfile(file_path):
            print(f"{file_path} does not exist.")
            return
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(address, port)
        client.connect((address, port))
        
        print(f"Sending {file_path} to {(address, port)}...")
        
        with open(file_path, "rb") as file:
            image_chunk = file.read(2048)
            while image_chunk:
                client.send(image_chunk)
                image_chunk = file.read(2048)
        
        client.send(f'IMAGE_END {duration}'.encode())

        print(f"Image successfully sent to {address}:{port}.")
        
        client.shutdown(socket.SHUT_WR)
        client.close()
        print("Socket closed.")
