import sys
from PyQt6.QtCore import Qt, QEvent, QFile, QTextStream, QDateTime, pyqtSignal, QRect, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar
)
from PyQt6.QtGui import QPixmap, QAction, QGuiApplication, QColor


from API import funzioni as f 
from PAGE import home_page as h, launcher_page as l, salva_peso_page as s, log_page as lo, diagnostic_page as d
from CMP import navbar as nv, Bilancia_diagno as b, Bilancia_diagno_deactive as bd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pagina di TEST")
        
        wid = QWidget()
        wid.setContentsMargins(0,0,0,0)
        v0 = QVBoxLayout(wid)
        v0.setSpacing(0)
        v0.setContentsMargins(0,0,0,0)
        
        nav = nv.NavbarWidget()
        
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.lista_bilance = []
        ogg = d.DiagnosticWidget(self)
        
        v0.addWidget(nav)
        v0.addWidget(ogg)
        
        self.setCentralWidget(wid)
        
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())