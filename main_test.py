import sys
from PyQt6.QtCore import Qt, QEvent, QFile, QTextStream, QSize,  QDateTime, pyqtSignal, QRect, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar
)
from PyQt6.QtGui import QPixmap, QAction, QColor

from API import funzioni as f 
from PAGE import home_page as h, launcher_page as l, salva_peso_page as s, log_page as lo, diagnostic_page as d
from CMP import navbar as nv, Bilancia_diagno as b, Bilancia_diagno_deactive as bd, loading as carica, loading2 as carica2


import time
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
        ogg = carica.QCustomPerlinLoader(
                                parent=self,
                                size=QSize(700, 400),
                                message="Caricamento...",
                                color=QColor("#000000"),
                                fontFamily="Ebrima",
                                fontSize=30,
                                rayon=200,
                                duration=60 * 1000,
                                noiseOctaves=0.8,
                                noiseSeed=int(time.time()),
                                backgroundColor=QColor("transparent"),
                                circleColor1=QColor("#E74C3C"),
                                circleColor2=QColor("#FD6363"),
                                circleColor3=QColor("#BDC3C7")
                            )
        
        ogg2 = carica2.QCustom3CirclesLoader(size=400)
        
        v0.addWidget(nav)
        v1 = QHBoxLayout()
        
        v1.addWidget(ogg)
        v1.addWidget(ogg2)
        
        v0.addLayout(v1)
        
        self.setCentralWidget(wid)
        self.set_background_color()
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241,241,241))
        self.setPalette(p)
        
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())