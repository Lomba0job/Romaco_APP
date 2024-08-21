import concurrent.futures
import threading
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy, QProgressBar, QLineEdit
from PyQt6.QtCore import Qt, QFile, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QSize
from PyQt6.QtGui import QColor, QPalette, QPixmap, QIcon
import time 

from CMP import rectangle as r, loading2 as carica, livello1 as l1, livello2 as l2
from API import funzioni as f, modbus_generico as mb

class Settings(QWidget):

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("Settings")
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        
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
        ico = f.get_img("logo.jpg")
        logo_label.setPixmap(QPixmap(ico).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))   
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
        self.sotto_menu = QVBoxLayout()
        
        self.h1 = QHBoxLayout()
        self.contro_label(0)
        self.main_layout.addLayout(self.h1)
        self.main_layout.addStretch()  
        self.sotto_menu.setContentsMargins(0,0,0,0)
        self.sotto_menu.setSpacing(0)
        self.main_layout.addLayout(self.sotto_menu)
        self.main_layout.addStretch()
    
    def contro_label(self, livello):
        exit = QPushButton()
        # Carica la pixmap
        logo_pixmap = QPixmap(f.get_img("back.png"))
        
        # Crea un'icona a partire dalla pixmap
        icon = QIcon(logo_pixmap)
        
        # Imposta l'icona sul pulsante
        exit.setIcon(icon)
        
        # Imposta la dimensione dell'icona sul pulsante (se necessario)
        exit.setIconSize(logo_pixmap.scaledToHeight(50).size())
        exit.setMaximumWidth(70)
        
        if( livello == 0):
            self.clearLayout(self.h1)
            self.h1.addWidget(exit)
            self.h1.addStretch()
            exit.clicked.connect(self.back_home)
        elif livello == 1: 
            self.clearLayout(self.h1)
            contro_conf = QLabel("LIVELLO 1   ")
            contro_conf.setObjectName("configurazione_label")
            contro_conf.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.h1.addWidget(exit)
            self.h1.addStretch()
            self.h1.addWidget(contro_conf)
            exit.clicked.connect(self.back_setting)
        elif livello == 2: 
            self.clearLayout(self.h1)
            contro_conf = QLabel("LIVELLO 2   ")
            contro_conf.setObjectName("configurazione_label")
            contro_conf.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.h1.addWidget(exit)
            self.h1.addStretch()
            self.h1.addWidget(contro_conf)
            exit.clicked.connect(self.back_setting)
        elif livello == 3: 
            self.clearLayout(self.h1)
            contro_conf = QLabel("Misurazione Contiuna")
            contro_conf.setObjectName("configurazione_label")
            contro_conf.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.h1.addWidget(exit)
            self.h1.addStretch()
            self.h1.addWidget(contro_conf)
            exit.clicked.connect(self.back_liv2)
        
        
        
        
    def log(self):
        
        wid = QWidget()
        ve = QVBoxLayout()
        h = QHBoxLayout()
        
        titolo = QLabel("AREA PRIVATA")
        titolo.setObjectName("titoloi")
        password = QLabel("password")
        password.setObjectName("pass")
        self.pass_text = QLineEdit()
        self.pass_text.setEchoMode(QLineEdit.EchoMode.Password)
        # Collegare il segnale returnPressed al metodo enter
        self.pass_text.returnPressed.connect(self.enter)
        
        
        x = QPushButton()
        logo_pixmap = QPixmap(f.get_img("X.png")) # Carica la pixmap
        icon = QIcon(logo_pixmap) # Crea un'icona a partire dalla pixmap
        x.setIcon(icon) # Imposta l'icona sul pulsante
        # Imposta la dimensione dell'icona sul pulsante (se necessario)
        x.setIconSize(logo_pixmap.scaledToHeight(40).size())
        x.setMaximumWidth(50)
        x.clicked.connect(self.canc)
        
        v = QPushButton()
        logo_pixmap = QPixmap(f.get_img("V.png"))  # Carica la pixmap
        icon = QIcon(logo_pixmap) # Crea un'icona a partire dalla pixmap
        v.setIcon(icon) # Imposta l'icona sul pulsante
        # Imposta la dimensione dell'icona sul pulsante (se necessario)
        v.setIconSize(logo_pixmap.scaledToHeight(40).size())
        v.setMaximumWidth(50)
        v.clicked.connect(self.enter)
        
        h.addStretch()
        h.addWidget(x)
        h.addWidget(v)
        
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        password.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        ve.addWidget(titolo)
        ve.addWidget(password)
        ve.addWidget(self.pass_text)
        ve.addLayout(h)
        
        wid.setLayout(ve)
        wid.setObjectName("wid")
        wid.setMaximumWidth(600)
        
        
        h2 = QHBoxLayout()
        h2.addStretch()
        h2.addWidget(wid)
        h2.addStretch()
        self.sotto_menu.addLayout(h2)
        self.sotto_menu.addStretch()
    
    def preUI(self):
        self.header()
        self.log()
        
        self.setLayout(self.main_layout)
        self.load_stylesheet()
        
    def UIlivello2(self):
        self.clearLayout(self.sotto_menu)
        self.contro_label(2)
        self.liv2 = l2.Livello2(self)
        self.sotto_menu.addWidget(self.liv2)
        self.sotto_menu.addStretch()
        
    def diagnosi_page(self):
        self.contro_label(3)
        
    def UIlivello1(self):
        self.clearLayout(self.sotto_menu)
        self.contro_label(1)
        self.liv1 = l1.Livello1(self)
        self.sotto_menu.addWidget(self.liv1)
        self.sotto_menu.addStretch()
        

    def canc(self):
        self.pass_text.setText("")
        
    def enter(self):
        if self.pass_text.text() == "IsolaNLV":
            print("livello1")
            self.UIlivello1()
        elif self.pass_text.text() == "NLVlombapass":
            print("livello2")
            self.UIlivello2()
        else:
            print("WRONG")
        self.canc()
        
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
                    
    def back_home(self):
        self.clearLayout(self.main_layout)
        self.preUI()
        self.master.back_home()
        
        
    def back_setting(self):
        self.clearLayout(self.main_layout)
        self.preUI()
        
    def back_liv2(self):
        self.UIlivello2()