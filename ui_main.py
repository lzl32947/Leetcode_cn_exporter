import sys

from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from util.settings import init_settings
from util.sql import SQLiteDriver

if __name__ == '__main__':
    # The main application
    init_settings()
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
    SQLiteDriver().close_all()
