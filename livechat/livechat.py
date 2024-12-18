import ctypes
import platform
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox

from .livechat_window import LiveChatWindow
from .popup import Popup
from .receiver import Receiver
from .register import Register
from .sender import Sender


class LiveChat(QApplication):
    def __init__(self, show_sender=True):
        super().__init__(sys.argv)
        
        # App settings
        if platform.system() == "Windows":
            myappid = 'maitrerenard.livechat.version'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        # Receiver
        self.image_receiver = Receiver()
        self.image_receiver.image_received.connect(self.show_popup, Qt.QueuedConnection)
        self.image_receiver.start()
        
        # Registry
        self.registry = {}
        
        self.user_register = Register()
        self.user_register.user_registered.connect(self.register_user, Qt.QueuedConnection)
        self.user_register.user_disconnected.connect(self.unregister_user, Qt.QueuedConnection)
        self.user_register.start()
        
        self.aboutToQuit.connect(self.user_register.send_disconnect)
        
        # Sender
        if show_sender:
            self.live_chat_window = LiveChatWindow()
            self.live_chat_window.send_image.connect(self.send_image, Qt.QueuedConnection)
            self.live_chat_window.refresh_registry.connect(self.refresh_registry, Qt.QueuedConnection)
            self.live_chat_window.show()

            self.image_sender = Sender()
        else:
            self.setQuitOnLastWindowClosed(False)
            
        self.sender_shown = show_sender
    
    def send_image(self, image_path: str, duration: int = 5) -> None:
        selected_users = self.live_chat_window.get_selected_users()
        
        if not selected_users:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(self.live_chat_window.windowIcon())
            msg.setText("No users selected.")
            msg.setWindowTitle("Live Chat")
            msg.exec()
        
        for user in selected_users:            
            address = self.registry[user]
            port = self.image_receiver.port
            
            print(f"Sending to {address}:{port}")
            self.image_sender.send_image(image_path, address=address, port=port, duration=duration)
    
    def refresh_registry(self) -> None:
        self.registry = {self.user_register.get_username(): self.user_register.get_ip()}
        self.user_register.send_username(discover=True)
        if self.sender_shown: self.live_chat_window.refresh_ui(self.registry)
                                                                                                                 
    def register_user(self, username: str, ip: str) -> None:
        self.registry[username] = ip
        if self.sender_shown: self.live_chat_window.refresh_ui(self.registry)
    
    def unregister_user(self, username: str) -> None:
        self.registry.pop(username)
        if self.sender_shown: self.live_chat_window.refresh_ui(self.registry)
    
    def show_popup(self, image_data: bytes, duration: float) -> None:
        try:
            popup = Popup(image_data, duration)
            popup.show_popup()
        
        except Exception as error:
            print(error)


def main() -> None:
    show_sender = True
    if len(sys.argv) > 1:
        match sys.argv[1].lower():
            case 'true':
                show_sender = True
            case 'false':
                show_sender = False
            case _:
                print("Invalid argument. Usage: livechat [show_sender]")
                sys.exit(1)
    
    app = LiveChat(show_sender)
    app.exec()

if __name__ == "__main__":
    main()
