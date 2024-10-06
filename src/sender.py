import os
import socket
import sys

from PyQt5.QtCore import QThread, pyqtSignal


class Sender(QThread):
    open_image = pyqtSignal()
    
    def run(self) -> None:
        input("Press any key to send an image...\n")
        self.open_image.emit()
    
    def send_image(self, file_path: str, address: str = "255.255.255.255", port: int = 5555, duration: float | int = 5) -> None:
        # Vérification de l'existence du fichier
        if not os.path.isfile(file_path):
            print(f"{file_path} does not exist.")
            return
        
        print(f"Sending {file_path}...")
        
        # Création du socket pour le client
        client = socket.socket(type=socket.SOCK_DGRAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Création de l'adresse
        addr = ("255.255.255.255", port)

        # Ouverture de l'image en mode binaire
        with open(file_path, "rb") as file:
            # Lecture et envoi de l'image par blocs
            image_chunk = file.read(2048)
            while image_chunk:
                client.sendto(image_chunk, addr)
                image_chunk = file.read(2048)

        # Envoi de la fin de l'image et la durée d'affichage
        client.sendto(b'IMAGE_END', addr)
        client.sendto(str(duration).encode(), addr)
        
        # Fermeture de la connexion
        print(f"Image successfully sent to {address}:{port}.")
        client.close()
