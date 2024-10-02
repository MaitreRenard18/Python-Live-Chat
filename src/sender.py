import os
import pathlib
import socket
import sys


def send_image_broadcast(file_path: str, duration: float = 5, port: int = 5555) -> None:
    # Vérification de l'existence du fichier
    if not os.path.isfile(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        return
    
    print(f"Envoi de l'image {file_path}...")
    
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
    print(f"Image envoyée avec succès à {addr[0]}:{addr[1]}.")
    client.close()


if __name__ == "__main__":
    send_image_broadcast(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 5, sys.argv[3] if len(sys.argv) > 3 else 5555)
