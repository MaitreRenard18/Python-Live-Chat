import os
import pathlib
import socket
import sys


def send_image_broadcast(file_path: str, port: int = 5555) -> None:
    if not os.path.isfile(file_path):
        print(f"Le fichier {file_path} n'existe pas")
        return
    
    print(f"Envoi de l'image {file_path}")
    
    # Création du socket pour le client
    client = socket.socket(type=socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Création de l'adresse
    addr = ("255.255.255.255", port)

    # Ouverture de l'image en mode binaire
    file = open(file_path, "rb")

    # Lecture et envoi de l'image par blocs
    image_chunk = file.read(2048)
    while image_chunk:
        client.sendto(image_chunk, addr)
        image_chunk = file.read(2048)

    client.sendto(b'END', addr)

    file.close()
    print("Image envoyée")

    # Fermeture de la connexion
    client.close()


if __name__ == "__main__":
    send_image_broadcast(sys.argv[1])
