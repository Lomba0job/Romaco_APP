import concurrent.futures
import threading
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy, QProgressBar
from PyQt6.QtCore import Qt, QFile, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QSize
from PyQt6.QtGui import QColor, QPalette, QPixmap
import time 

from CMP import rectangle as r, loading2 as carica
from API import funzioni as f, modbus_generico as mb

class Settings(QWidget):

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("Settings")
        
        
        self.preUI()
        self.setAutoFillBackground(True)
        self.set_background_color()
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(254,254,254))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("settings.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)
            
            
    def header(self):
        
        # Header
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap(f.get_img("logo.jpg"))
        logo_label.setPixmap(logo_pixmap.scaledToHeight(50))
        header_layout.addWidget(logo_label)

        title_label = QLabel("NANO<span style='color:#E74C3C'>LEVER</span>")
        title_label.setObjectName("title_label")
        header_layout.addWidget(title_label)

        subtitle_label = QLabel("SISTEMA AD ISOLA")
        subtitle_label.setObjectName("subtitle_label")
        header_layout.addWidget(subtitle_label)

        header_layout.addStretch()
        
        configurazione_label = QLabel("IMPOSTAZIONI")
        configurazione_label.setObjectName("configurazione_label")
        header_layout.addWidget(configurazione_label)

        wid = QWidget()
        wid.setObjectName("menulab")
        wid.setLayout(header_layout)
        wid.setMaximumHeight(100)
        wid.setAutoFillBackground(True)
        self.main_layout.addWidget(wid)
    
    def preUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.header()
        
        
        exit = QPushButton("esci")
        exit.setObjectName("puls")
        exit.clicked.connect(self.master.back_home)
        self.main_layout.addStretch()
        self.main_layout.addWidget(exit)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)
        self.load_stylesheet()
