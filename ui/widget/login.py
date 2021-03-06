from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class UserNameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.input_username = QLineEdit()
        self.inner_layout = QHBoxLayout()
        self.setLayout(self.inner_layout)
        self.inner_layout.addWidget(QLabel("Username:"))
        self.inner_layout.addWidget(self.input_username)

    def get_input(self) -> str:
        """
        Get the input from the lineEdit
        :return: str, the input text
        """
        return self.input_username.text()


class PasswordWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.input_passwd = QLineEdit()
        self.inner_layout = QHBoxLayout()
        self.setLayout(self.inner_layout)
        self.inner_layout.addWidget(QLabel("Password:"))
        self.inner_layout.addWidget(self.input_passwd)

    def get_input(self):
        """
        Get the input from the lineEdit
        :return: str, the input text
        """
        return self.input_passwd.text()


class LoginWidget(QWidget):
    # The signal for transferring the user and passwd
    login_signal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        # Define the two widgets
        self.user_name_widget = UserNameWidget()
        self.passwd_widget = PasswordWidget()
        # Add button
        self.login_button = QPushButton("Login")
        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.user_name_widget)
        layout.addWidget(self.passwd_widget)
        layout.addWidget(self.login_button)
        self.setLayout(layout)
        # Set Clicked
        self.login_button.clicked.connect(self.login_click_event)

    # Triggered by the "login_button.clicked"
    def login_click_event(self):
        user_name = self.user_name_widget.get_input()
        passwd = self.passwd_widget.get_input()
        if user_name == "" or passwd == "":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Invalid input!")
            dlg.setText("You must input the valid username and passwd!")
            button = dlg.exec()
        else:
            self.login_signal.emit((user_name, passwd))
