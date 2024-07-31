import sys
from PyQt6.QtCore import Qt, QEvent, QFile, QTextStream, QDateTime, pyqtSignal, QRect, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar
)
from PyQt6.QtGui import QPixmap, QAction, QGuiApplication

from PAGE import home_page as h, launcher_page as l, salva_peso_page as s
from CMP import navbar as nv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pagina di TEST")
        
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        
        ogg = s.SalvaPesoWidget(self)
        
        self.setCentralWidget(ogg)
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())