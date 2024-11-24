import os
import platform
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QShortcut, QWidget

from .utils import get_file_from_url, resource_path


class LiveChatWindow(QWidget):
    send_image = pyqtSignal(str, float)
    
    def __init__(self, app):
        super().__init__()
        
        uic.loadUi(resource_path(resource_path('ui/livechat V2.ui')), self)
        self.setWindowTitle("Live Chat")
        self.setWindowIcon(QtGui.QIcon(resource_path('assets/icon' + ".ico" if platform.system() == "Windows" else '.png')))

        self.app = app

        self.refresh_list_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.refresh_list_shortcut.activated.connect(self.force_refresh)

        self.open_image_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.open_image_shortcut.activated.connect(self.on_open)

        self.browse_button.clicked.connect(self.on_open)
        self.refresh_button.clicked.connect(self.force_refresh)
        self.send_button.clicked.connect(self.on_send)

    def force_refresh(self):
        self.app.refresh_registry()
        self.refresh()
    
    def refresh(self):
        self.users_list.clear()
        
        for user in self.app.registry.keys():
            item = QtWidgets.QListWidgetItem(user)
            item.setCheckState(Qt.Unchecked)
            item.setForeground(QtGui.QColor(255, 255, 255))
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self.users_list.addItem(item)
    
    def get_selected_users(self):
        for i in range(self.users_list.count()):
            if self.users_list.item(i).checkState() == Qt.Checked:
                yield self.users_list.item(i).text()
    
    def on_open(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, caption="Open Image", filter="Image Files (*.png *.jpg *.jpeg *.gif *.mp4)")
        
        if file_path:
            self.image_path.setPlainText(file_path)
        else:
            print("No file selected.")
            
    def on_send(self):
        try:
            path = get_file_from_url(self.image_path.toPlainText())
            self.send_image.emit(path, self.duration_box.value())
        except Exception as e:
            print("Invalid URL or file path.", e)
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowIcon(self.windowIcon())
            msg.setText("Invalid URL or file path.")
            msg.setWindowTitle("Live Chat")
            msg.exec()
