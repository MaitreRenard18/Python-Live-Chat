import socket

import pytest

from src import Receiver, Sender

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
    ("", 0),
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
