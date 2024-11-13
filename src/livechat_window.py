import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QLabel, QShortcut, QWidget


class LiveChatWindow(QWidget):
    send_image = pyqtSignal(str, float)
    
    def __init__(self, app):
        super().__init__()
        
        self.setWindowTitle("Live Chat")
        self.setWindowIcon(QtGui.QIcon('assets/icon.png'))
        self.setupUi()

        self.app = app

        self.refresh_list_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.refresh_list_shortcut.activated.connect(self.force_refresh)

        self.open_image_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.open_image_shortcut.activated.connect(self.on_open)

        self.pushButton.clicked.connect(self.on_open)
        self.pushButton_2.clicked.connect(self.force_refresh)
    
    def force_refresh(self):
        self.app.refresh_registry()
        self.refresh()
    
    def refresh(self):
        self.listWidget.clear()
        
        for user in self.app.registry.keys():
            item = QtWidgets.QListWidgetItem(user)
            item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)
    
    def get_selected_users(self):
        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).checkState() == Qt.Checked:
                yield self.listWidget.item(i).text()
    
    def on_open(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        
        if file_path:
            self.send_image.emit(file_path, self.doubleSpinBox.value())
        else:
            print("No file selected.")
    
    # Generated by Qt Designer
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(550, 275)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: rgb(12, 15, 29);")
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 24))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 32))
        self.frame.setSizeIncrement(QtCore.QSize(0, 0))
        self.frame.setBaseSize(QtCore.QSize(0, 0))
        self.frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMaximumSize(QtCore.QSize(16, 16))
        self.frame_2.setStyleSheet("border-radius: 8px;\n"
"background-color: rgb(85, 255, 0);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout.addWidget(self.frame_2)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setHintingPreference(QtGui.QFont.HintingPreference.PreferNoHinting)
        font.setFamily("Yu Gothic UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.frame)
        self.line = QtWidgets.QFrame(self)
        self.line.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line.setStyleSheet("border: 1px solid white;\n"
"border-style: inset;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self)
        self.label.setMinimumSize(QtCore.QSize(0, 24))
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(16, 24))
        self.pushButton_2.setMaximumSize(QtCore.QSize(64, 32))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"                                        background-color: #1a224d; \n"
"                                        border: none;\n"
"                                        border-radius: 8px;\n"
"                                        color: #556de5;\n"
"                                      }\n"
"                                      QPushButton:hover {\n"
"                                        color: #f0f0f0;\n"
"                                        background-color: #556de5;\n"
"                                      }")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setStyleSheet("border: none;")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.doubleSpinBox.setMinimumSize(QtCore.QSize(16, 24))
        self.doubleSpinBox.setMaximumSize(QtCore.QSize(128, 32))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.doubleSpinBox.setFont(font)
        self.doubleSpinBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.doubleSpinBox.setStyleSheet("background-color: #1a224d; \n"
"border: none;\n"
"border-radius: 8px;\n"
"color: #556de5;\n"
"")
        self.doubleSpinBox.setWrapping(False)
        self.doubleSpinBox.setFrame(True)
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox.setAccelerated(False)
        self.doubleSpinBox.setKeyboardTracking(True)
        self.doubleSpinBox.setProperty("showGroupSeparator", False)
        self.doubleSpinBox.setMaximum(1000.0)
        self.doubleSpinBox.setProperty("value", 5.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout_2.addWidget(self.doubleSpinBox)
        self.pushButton = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(16, 24))
        self.pushButton.setMaximumSize(QtCore.QSize(512, 32))
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton {\n"
"                                        background-color: #1a224d; \n"
"                                        border: none;\n"
"                                        border-radius: 8px;\n"
"                                        color: #556de5;\n"
"                                      }\n"
"                                      QPushButton:hover {\n"
"                                        color: #f0f0f0;\n"
"                                        background-color: #556de5;\n"
"                                      }")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Receiver Online"))
        self.label.setText(_translate("Form", "Connected users"))
        self.pushButton_2.setText(_translate("Form", "Refresh"))
        self.pushButton.setText(_translate("Form", "Send Image"))
