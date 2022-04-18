from typing import Any, Optional, List

from PyQt6.QtCore import pyqtSignal, QThreadPool
from PyQt6.QtWidgets import *

from ui.runnable.WorkerThread import Worker
from ui.runnable.login_runnable import login_via_browser
from ui.runnable.output_runnable import output_to_files
from ui.runnable.tag_runnable import list_tags
from ui.widget.login import LoginWidget
from ui.widget.status import StatusWidget
from util.sql import SQLiteDriver


class InnerStatusWidget(QWidget):
    login_signal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.login_widget = LoginWidget()
        self.login_widget.login_signal.connect(self.login_event)
        self.state_widget = StatusWidget()
        layout = QStackedLayout()
        layout.addWidget(self.login_widget)
        layout.addWidget(self.state_widget)
        self.setLayout(layout)

    def change_to_logined(self):
        self.layout().setCurrentIndex(1)
        self.state_widget.set_username(self.login_widget.user_name_widget.get_input())

    def login_event(self, user_passwd_tuple):
        self.login_signal.emit(user_passwd_tuple)


class OperationPanelWidget(QWidget):
    output_signal = pyqtSignal()
    tag_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.output_button = QPushButton("Export the record")
        self.output_button.clicked.connect(self.on_output_clicked)
        self.tag_button = QPushButton("Export tags")
        self.tag_button.clicked.connect(self.on_tag_clicked)
        layout.addWidget(self.output_button)
        layout.addWidget(self.tag_button)
        self.setLayout(layout)

    def on_output_clicked(self):
        self.output_signal.emit()

    def on_tag_clicked(self):
        self.tag_signal.emit()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cookies_store = None
        self.store_problems = None
        self.left_widget = InnerStatusWidget()
        self.left_widget.login_signal.connect(self.login_event)
        self.right_widget = OperationPanelWidget()
        self.right_widget.output_signal.connect(self.output_record_event)
        self.right_widget.tag_signal.connect(self.tag_output_event)
        layout = QHBoxLayout()
        layout.addWidget(self.left_widget)
        layout.addWidget(self.right_widget)
        self.setLayout(layout)
        self.dlg = QMessageBox()

    def tag_output_event(self):
        if self.store_problems is None or self.cookies_store is None:
            button = QMessageBox.critical(
                self,
                "Please Login and Output Problems",
                "Please both login and output the problems first!",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
        else:
            SQLiteDriver().create_conn("general")
            renew_id_and_link = SQLiteDriver().find_problem_not_exist_tag("general")
            worker = Worker(list_tags, self.cookies_store, renew_id_and_link)
            worker.signals.finished.connect(self.tag_event_finish)
            QThreadPool.globalInstance().start(worker)
            self.dlg.setWindowTitle("Exporting")
            self.dlg.setText("Exporting your tags from leetcode-cn.com, please wait for a few seconds...")
            self.dlg.exec()

    def tag_event_finish(self):
        self.dlg.close()
        QMessageBox.information(
            self,
            "Finish",
            "Export Finish.\nAll tags has been exported.",
            buttons=QMessageBox.StandardButton.Ok,
            defaultButton=QMessageBox.StandardButton.Ok,
        )

    def output_record_event(self):
        if self.cookies_store is None:
            button = QMessageBox.critical(
                self,
                "Please Login",
                "Please enter your name and passwd to login first!",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
        else:
            worker = Worker(output_to_files, self.cookies_store)
            worker.signals.result.connect(self.output_event_result)
            worker.signals.finished.connect(self.output_event_finish)
            QThreadPool.globalInstance().start(worker)
            self.dlg.setWindowTitle("Exporting")
            self.dlg.setText("Exporting your record from leetcode-cn.com, please wait for a few seconds...")
            self.dlg.exec()

    def output_event_result(self, result: Optional[List[tuple]]):
        self.store_problems = result
        if result is not None:
            SQLiteDriver().create_conn("general")
            SQLiteDriver().insert_into_problems("general", result)

    def output_event_finish(self):
        self.dlg.close()
        button = QMessageBox.information(
            self,
            "Finish",
            "Export Finish.\nYou can find it in \"output\" directory.",
            buttons=QMessageBox.StandardButton.Ok,
            defaultButton=QMessageBox.StandardButton.Ok,
        )

    def login_event(self, user_passwd_tuple):
        user = user_passwd_tuple[0]
        passwd = user_passwd_tuple[1]
        worker = Worker(login_via_browser, user=user, passwd=passwd)
        worker.signals.result.connect(self.login_event_result)
        QThreadPool.globalInstance().start(worker)
        self.dlg.setWindowTitle("Login...")
        self.dlg.setText("Logging yourself into leetcode-cn.com, please wait for a few seconds...")
        self.dlg.exec()

    def login_event_result(self, result: Optional[Any]):
        self.dlg.close()
        if result is None:

            button = QMessageBox.critical(
                self,
                "Login Fail!",
                "Fail to login to leetcode-cn.com.",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
        else:
            self.cookies_store = result
            button = QMessageBox.information(
                self,
                "Login success!",
                "Successfully login to leetcode-cn.com!",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            self.left_widget.change_to_logined()
