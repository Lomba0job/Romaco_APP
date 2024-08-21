import concurrent.futures
import threading
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy, QProgressBar, QLineEdit, QStackedWidget
from PyQt6.QtCore import Qt, QFile, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QSize
from PyQt6.QtGui import QColor, QPalette, QPixmap, QIcon

from CMP import rectangle as r, loading2 as carica, livello1 as l1, livello2 as l2
from API import funzioni as f, modbus_generico as mb


class Header(QWidget):
    def __init__(self, master):
       
        super().__init__() 
        self.master = master
        
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

        self.h1 = QHBoxLayout()
        self.contro_label(0, master)
        
        mast_l = QVBoxLayout()
        mast_l.addLayout(header_layout)
        mast_l.addLayout(self.h1)
        
        self.setLayout(mast_l)
        self.setMaximumHeight(150)
        self.setAutoFillBackground(True)
        self.set_background_color()
        
    def contro_label(self, livello, master):
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
            exit.clicked.connect(master.back_home)
        elif livello == 1: 
            self.clearLayout(self.h1)
            contro_conf = QLabel("LIVELLO 1   ")
            contro_conf.setObjectName("configurazione_label")
            contro_conf.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.h1.addWidget(exit)
            self.h1.addStretch()
            self.h1.addWidget(contro_conf)
            exit.clicked.connect(master.back_setting)
        elif livello == 2: 
            self.clearLayout(self.h1)
            contro_conf = QLabel("LIVELLO 2   ")
            contro_conf.setObjectName("configurazione_label")
            contro_conf.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.h1.addWidget(exit)
            self.h1.addStretch()
            self.h1.addWidget(contro_conf)
            exit.clicked.connect(master.back_setting)
        elif livello == 3: 
            self.clearLayout(self.h1)
            contro_conf = QLabel("Misurazione Contiuna")
            contro_conf.setObjectName("configurazione_label")
            contro_conf.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.h1.addWidget(exit)
            self.h1.addStretch()
            self.h1.addWidget(contro_conf)
            exit.clicked.connect(master.back_liv2)
        
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(254,254,254))
        self.setPalette(p)
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("settings.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)
    
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())


class Home_Impo(QWidget):
    
    def __init__(self, master):
       
        super().__init__() 
        self.master = master
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
        
        
        l = QVBoxLayout()
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addStretch()
        l.addWidget(wid)
        l.addStretch()
        
        self.setLayout(l)
        self.setAutoFillBackground(True)
        self.set_background_color()
        
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(254,254,254))
        self.setPalette(p)
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("settings.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)
        
    def enter(self):
        if self.pass_text.text() == "IsolaNLV":
            self.master.stacked_widget.setCurrentIndex(1)  # Livello1
        elif self.pass_text.text() == "NLVlombapass":
            self.master.stacked_widget.setCurrentIndex(2)  # Livello2
        else:
            print("WRONG")
        self.canc()
        
    def canc(self):
        self.pass_text.setText("")
        
        

class Settings(QWidget):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.setWindowTitle("Settings")
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        
        self.head = Header(self)
        self.main_layout.addWidget(self.head)
        
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        self.preUI()
        self.setLayout(self.main_layout)
        self.setAutoFillBackground(True)
        self.set_background_color()
        
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(254,254,254))
        self.setPalette(p)
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("settings.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)

    def preUI(self):
    
        self.home_page = Home_Impo(self)
        self.stacked_widget.addWidget(self.home_page)
        
        self.liv1_page = l1.Livello1(self)
        self.stacked_widget.addWidget(self.liv1_page)
        
        self.liv2_page = l2.Livello2(self)
        self.stacked_widget.addWidget(self.liv2_page)
        
        self.stacked_widget.setCurrentIndex(0)
        
    
    def back_home(self):
        self.master.back_home()  # Home
        
    def back_setting(self):
        self.contro_label(0)
        self.stacked_widget.setCurrentIndex(0)  # Home
        
    def back_liv2(self):
        self.contro_label(2)
        self.liv2_page.home()
        self.stacked_widget.setCurrentIndex(2)  # Livello2
        
    def back_liv1(self):
        self.contro_label(1)
        self.liv1_page.home()
        self.stacked_widget.setCurrentIndex(1)  # Livello1

    def contro_label(self, livello):
        self.head.contro_label(livello, self)