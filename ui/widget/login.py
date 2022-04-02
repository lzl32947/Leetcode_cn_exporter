from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

from ui.runnable.login_thread import LoginThread


class UserNameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.input_username = QLineEdit()
        self.inner_layout = QHBoxLayout()
        self.setLayout(self.inner_layout)
        self.inner_layout.addWidget(QLabel("Username:"))
        self.inner_layout.addWidget(self.input_username)

    def get_input(self):
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
        return self.input_passwd.text()


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.user_name_widget = UserNameWidget()
        self.passwd_widget = PasswordWidget()
        self.inner_layout = QVBoxLayout()
        self.setLayout(self.inner_layout)
        self.login_button = QPushButton("Login")
        self.inner_layout.addWidget(self.user_name_widget)
        self.inner_layout.addWidget(self.passwd_widget)
        self.inner_layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.login_thread)

    def login_state(self, result):
        print(result)

    def login_thread(self):
        username = self.user_name_widget.get_input()
        passwd = self.passwd_widget.get_input()

        _thread = LoginThread(username=username, passwd=passwd)
        _thread.signals.result.connect(self.login_state)
        self.threadpool.start(_thread)
