import pytest

from src import Receiver, Sender


@pytest.mark.parametrize("image_path", ["tests/data/test_image_0.jpg"])
def test_sender_receiver(image_path: str) -> None:
    receiver = Receiver(port=5050)
    receiver.start()
    
    sender = Sender()
    sender.send_image(file_path="tests/data/test_image_0.jpg", address="0.0.0.0", port=5050, duration=5)
    