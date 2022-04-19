from typing import Any, Optional, List

from PyQt6.QtCore import pyqtSignal, QThreadPool
from PyQt6.QtWidgets import *

from ui.runnable.WorkerThread import Worker
from ui.runnable.export_runnable import export_from_sql_to_xlsx
from ui.runnable.login_runnable import login_via_browser
from ui.runnable.output_runnable import output_problem_to_sqls
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
    problem_signal = pyqtSignal()
    export_signal = pyqtSignal()
    tag_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.output_button = QPushButton("Download the solved problems")
        self.output_button.clicked.connect(self.on_output_clicked)
        self.tag_button = QPushButton("Download the corresponding tags")
        self.tag_button.clicked.connect(self.on_tag_clicked)
        self.export_button = QPushButton("Export the previous")
        self.export_button.clicked.connect(self.on_export_clicked)
        layout.addWidget(self.output_button)
        layout.addWidget(self.tag_button)
        layout.addWidget(self.export_button)
        self.setLayout(layout)

    def on_output_clicked(self):
        self.problem_signal.emit()

    def on_tag_clicked(self):
        self.tag_signal.emit()

    def on_export_clicked(self):
        self.export_signal.emit()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cookies_store = None
        self.store_problems = None
        self.left_widget = InnerStatusWidget()
        self.left_widget.login_signal.connect(self.login_event)
        self.right_widget = OperationPanelWidget()
        self.right_widget.problem_signal.connect(self.store_solved_problems_event)
        self.right_widget.tag_signal.connect(self.store_tags_event)
        self.right_widget.export_signal.connect(self.export_from_db_event)
        layout = QHBoxLayout()
        layout.addWidget(self.left_widget)
        layout.addWidget(self.right_widget)
        self.setLayout(layout)
        self.dlg = QMessageBox()

    def export_from_db_event(self):
        SQLiteDriver().create_conn("general")
        worker = Worker(export_from_sql_to_xlsx, "general")
        worker.signals.finished.connect(self.export_from_db_event_finished)
        QThreadPool.globalInstance().start(worker)
        self.dlg.setWindowTitle("Exporting")
        self.dlg.setText("Exporting from database, please wait for a few seconds...")
        self.dlg.exec()

    def export_from_db_event_finished(self):
        self.dlg.close()
        QMessageBox.information(
            self,
            "Finish",
            "Export Finish.\nSee the \"output\" directory for output.",
            buttons=QMessageBox.StandardButton.Ok,
            defaultButton=QMessageBox.StandardButton.Ok,
        )

    def store_tags_event(self):
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

    def store_solved_problems_event(self):
        if self.cookies_store is None:
            button = QMessageBox.critical(
                self,
                "Please Login",
                "Please enter your name and passwd to login first!",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
        else:
            worker = Worker(output_problem_to_sqls, self.cookies_store)
            worker.signals.result.connect(self.store_solved_problems_event_result)
            worker.signals.finished.connect(self.store_solved_problems_event_finish)
            QThreadPool.globalInstance().start(worker)
            self.dlg.setWindowTitle("Exporting")
            self.dlg.setText("Exporting your solved problems from leetcode-cn.com, please wait for a few seconds...")
            self.dlg.exec()

    def store_solved_problems_event_result(self, result: Optional[List[tuple]]):
        self.store_problems = result
        if result is not None:
            SQLiteDriver().create_conn("general")
            SQLiteDriver().insert_into_problems("general", result)

    def store_solved_problems_event_finish(self):
        self.dlg.close()
        button = QMessageBox.information(
            self,
            "Finish",
            "Export Finish.\nAll your solved problems are stores in database.",
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
