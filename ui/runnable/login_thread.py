import sys
import traceback

from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal

from functional.process.login_process import LoginProcess


class LoginSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class LoginThread(QRunnable):

    def __init__(self, username, passwd):
        super(LoginThread, self).__init__()
        self.username = username
        self.passwd = passwd
        self.signals = LoginSignals()

    @pyqtSlot()
    def run(self):
        try:
            res = LoginProcess().run(user=self.username, passwd=self.passwd)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(res)
        finally:
            self.signals.finished.emit()
