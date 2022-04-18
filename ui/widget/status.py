from PyQt6.QtWidgets import *


class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.welcome_line = QLabel("Welcome:")
        self.information_line = QLabel()
        layout = QHBoxLayout()
        layout.addWidget(self.welcome_line)
        layout.addWidget(self.information_line)
        self.setLayout(layout)

    def set_username(self, name: str):
        self.information_line.setText(name)
