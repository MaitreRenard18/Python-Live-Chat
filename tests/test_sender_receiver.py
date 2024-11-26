import socket
from urllib import request

import pytest

from livechat import Receiver, Sender
from livechat.livechat_window import LiveChatWindow

IP = socket.gethostbyname(socket.gethostname())


@pytest.fixture
def receiver():
    receiver_instance = Receiver(port=5050)
    yield receiver_instance
    receiver_instance.close()
    receiver_instance.terminate()


@pytest.fixture
def sender():
    return Sender()


@pytest.mark.parametrize("image_path, duration", [
    ("tests/data/test_image_0.png", 10),
    ("tests/data/test_image_0.png", -5),
    ("tests/data/test_image_1.jpg", 0.5),
    ("tests/data/test_image_2.jpeg", 2 ** 16),
    ("", 0), # TODO Add error handling
    ("tests/data/test_gif_0.gif", 0),
])
def test_sender_receiver(receiver: Receiver, sender: Sender, image_path: str, duration: float) -> None:
    def _receive_data(received_image: bytes, received_duration: float) -> None:
        with open(image_path, "rb") as file:
            assert received_image == file.read()
        
        assert received_duration == duration

    receiver.image_received.connect(_receive_data)
    receiver.start()

    sender.send_image(file_path=image_path, address=IP, port=5050, duration=duration)


@pytest.mark.parametrize("url, duration", [
    ("https://www.ikea.com/fr/fr/images/products/blahaj-peluche-requin__0710175_pe727378_s5.jpg", -5),
    ("https://media1.tenor.com/m/Z6gmDPeM6dgAAAAC/dance-moves.gif", 10),
])
def test_sender_receiver_url(receiver: Receiver, sender: Sender, url: str, duration: float) -> None:
    def _receive_data(received_image: bytes, received_duration: float) -> None:
        with open(LiveChatWindow.get_file_from_url(url), "rb") as file:
            assert received_image == file.read()
        
        assert received_duration == duration
        
    receiver.image_received.connect(_receive_data)
    receiver.start()
    
    sender.send_image(file_path=LiveChatWindow.get_file_from_url(url), address=IP, port=5050, duration=duration)
