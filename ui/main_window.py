from PyQt6.QtWidgets import QMainWindow

from ui.widget.main_widget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LeetCode CN Exporter")
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)
