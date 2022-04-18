import sys

from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from util.settings import init_settings

if __name__ == '__main__':
    # The main application
    init_settings()
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
