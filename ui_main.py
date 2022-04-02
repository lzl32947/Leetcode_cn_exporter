import sys

from PyQt6.QtWidgets import QApplication

from config.enums import Browser
from config.options import Options
from ui.main_window import MainWindow
from util.drivers import Driver

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Driver().init(Browser.EDGE, Options().get_option(Browser.EDGE))
    window = MainWindow()
    window.show()

    app.exec()
