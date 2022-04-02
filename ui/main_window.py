from PyQt6.QtWidgets import QMainWindow, QStackedLayout, QWidget

from ui.widget.login import LoginWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LeetCode CN Exporter")
        layout = QStackedLayout()
        layout.addWidget(LoginWidget())
        layout.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
