from PyQt6.QtCore import pyqtSignal, QThreadPool
from PyQt6.QtWidgets import *

from config.enums import Browser
from config.options import Options
from config.url import MAIN_PAGE_URL
from functional.export.pandas_support import export_to_excel
from functional.parse.count_parse import parse_count_done
from functional.process.count_process import CountProcess
from functional.process.login_process import LoginProcess
from ui.runnable.WorkerThread import Worker
from ui.widget.login import LoginWidget
from ui.widget.status import StatusWidget
from util.drivers import Driver


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

    def login_event(self, user_passwd_tuple):
        self.login_signal.emit(user_passwd_tuple)


class OperationPanelWidget(QWidget):
    output_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.output_button = QPushButton("Export the record")
        self.output_button.clicked.connect(self.on_output_clicked)
        layout.addWidget(self.output_button)
        self.setLayout(layout)

    def on_output_clicked(self):
        self.output_signal.emit()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.cookies_store = None
        self.left_widget = InnerStatusWidget()
        self.left_widget.login_signal.connect(self.login_event)
        self.right_widget = OperationPanelWidget()
        self.right_widget.output_signal.connect(self.output_record_event)
        layout = QHBoxLayout()
        layout.addWidget(self.left_widget)
        layout.addWidget(self.right_widget)
        self.setLayout(layout)
        self.dlg = QMessageBox()

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
            worker = Worker(self.output_to_files)
            worker.signals.result.connect(self.output_finish)
            QThreadPool.globalInstance().start(worker)
            self.dlg.setWindowTitle("Exporting")
            self.dlg.setText("Exporting your record from leetcode-cn.com, please wait for a few seconds...")
            self.dlg.exec()

    def output_finish(self):
        self.dlg.close()

        button = QMessageBox.information(
            self,
            "Finish",
            "Export Finish.\nYou can find it in \"output\" directory.",
            buttons=QMessageBox.StandardButton.Ok,
            defaultButton=QMessageBox.StandardButton.Ok,
        )

    def output_to_files(self):
        Driver().init(Browser.EDGE, Options().get_option(Browser.EDGE))
        Driver().set_cookies(self.cookies_store, MAIN_PAGE_URL)
        result = CountProcess().run()
        Driver().close()
        if result[0]:
            parse_result = parse_count_done(result[1])
            export_to_excel("done", parse_result)

    def login_event(self, user_passwd_tuple):
        user = user_passwd_tuple[0]
        passwd = user_passwd_tuple[1]
        worker = Worker(self.login_via_browser, user=user, passwd=passwd)
        worker.signals.result.connect(self.print_output)
        QThreadPool.globalInstance().start(worker)
        self.dlg.setWindowTitle("Login...")
        self.dlg.setText("Logging yourself into leetcode-cn.com, please wait for a few seconds...")
        self.dlg.exec()

    def print_output(self):
        self.dlg.close()
        if self.cookies_store is None:
            button = QMessageBox.critical(
                self,
                "Login Fail!",
                "Fail to login to leetcode-cn.com.",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
        else:
            button = QMessageBox.information(
                self,
                "Login success!",
                "Successfully login to leetcode-cn.com!",
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )

    def login_via_browser(self, user: str, passwd: str):
        Driver().init(Browser.EDGE, Options().get_option(Browser.EDGE))
        result = LoginProcess().run(user=user, passwd=passwd)
        Driver().close()
        if result[0]:
            self.cookies_store = result[1]
