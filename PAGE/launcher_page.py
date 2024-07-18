from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal

class LauncherWidget(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("Pagina di Avvio")
        layout.addWidget(label)

        button = QPushButton("Vai alla Home")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button)

        self.setLayout(layout)

    def on_button_clicked(self):
        self.finished.emit()