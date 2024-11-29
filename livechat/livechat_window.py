import imghdr
import os
import platform
import sys
import tempfile
import urllib.request

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QShortcut, QWidget


class LiveChatWindow(QWidget):
    send_image = pyqtSignal(str, float)
    refresh_registry = pyqtSignal()
    
    def __init__(self) -> None:
        super().__init__()
        
        uic.loadUi(LiveChatWindow.resource_path('livechat/ui/livechat.ui'), self)
        self.setWindowTitle("Live Chat")
        self.setWindowIcon(QtGui.QIcon(LiveChatWindow.resource_path('assets/icons/icon' + ".ico" if platform.system() == "Windows" else '.png')))

        self.refresh_list_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.refresh_list_shortcut.activated.connect(self.force_refresh)

        self.open_image_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.open_image_shortcut.activated.connect(self.on_open)

        self.send_image_shortcut = QShortcut(QKeySequence("Ctrl+Enter"), self)
        self.send_image_shortcut.activated.connect(self.on_send)

        self.refresh_button.clicked.connect(self.force_refresh)
        self.browse_button.clicked.connect(self.on_open)
        self.send_button.clicked.connect(self.on_send)

    @staticmethod
    def resource_path(relative_path: str) -> str:
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)
    
    def force_refresh(self) -> None:
        self.refresh_registry.emit()
    
    def refresh_ui(self, registry: dict[str, str]) -> None:
        self.users_list.clear()
        
        for user in registry.keys():
            item = QtWidgets.QListWidgetItem(user)
            item.setCheckState(Qt.Unchecked)
            item.setForeground(QtGui.QColor(255, 255, 255))
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self.users_list.addItem(item)
    
    def get_selected_users(self) -> list[str]:
        users = []
        for i in range(self.users_list.count()):
            if self.users_list.item(i).checkState() == Qt.Checked:
                users.append(self.users_list.item(i).text())
                
        return users
    
    def on_open(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, caption="Open Image", filter="Image Files (*.png *.jpg *.jpeg *.gif)")
        
        if file_path:
            self.image_path.setPlainText(file_path)
        else:
            print("No file selected.")
    
    @staticmethod
    def get_file_from_url(url: str) -> str:
        if os.path.exists(url):
            return url

        request = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })
        
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(urllib.request.urlopen(request).read())
            return temp.name
    
    def on_send(self) -> None:
        try:
            path = LiveChatWindow.get_file_from_url(self.image_path.toPlainText())
            
            if not imghdr.what(path):
                raise Exception("Unsupported media type")
            
            self.send_image.emit(path, self.duration_box.value())

        except Exception as e:
            print("Invalid URL or file path.", e)
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(self.windowIcon())
            msg.setText("Invalid URL or file path.")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Live Chat")
            msg.exec()
