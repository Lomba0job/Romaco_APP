from PyQt6.QtCore import Qt, QFile, QTextStream, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QPushButton, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QFrame, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar, 
    QSpinBox, QRadioButton
)
from PyQt6.QtGui import QPixmap, QAction, QIcon, QColor
import os 

from PAGE import setting_page as s
from API import funzioni as f
from CMP import puls_livello2 as p 

class Livello2(QWidget):
    def __init__(self, master):
        super().__init__()
        
        self.master:s.Settings = master
        
        self.main_layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        
        self.home_page()
        self.diagnosi_page()
        
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)
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
    
    def home_page(self):
        home_widget = QWidget()
        home_layout = QVBoxLayout()
        home_widget.setLayout(home_layout)
        
        p1 = p.ClickableWidget(f.get_img("DIAGNOSI.png"), "Misurazione Continua")
        p1.clicked.connect(self.show_diagnosi_page)
        
        p2 = p.ClickableWidget(f.get_img("PARAM_SET.png"), "Settaggio Parametri")
        
        p3 = p.ClickableWidget(f.get_img("DB_F.png"), "Fuzioni Database")
        
        p4 = p.ClickableWidget(f.get_img("LOG_DATA.png"), "Funzioni DataLog")
        
        p5 = p.ClickableWidget(f.get_img("MOD_IMPO.png"), "Funzioni Mod-Bus")
        
        home_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        home_layout.addStretch()
        home_layout.addWidget(p1)
        home_layout.addSpacing(10)
        home_layout.addWidget(p2)
        home_layout.addSpacing(10)
        home_layout.addWidget(p3)
        home_layout.addSpacing(10)
        home_layout.addWidget(p4)
        home_layout.addSpacing(10)
        home_layout.addWidget(p5)
        home_layout.addStretch()
        
        self.stacked_widget.addWidget(home_widget)
        
    def diagnosi_page(self):
        diagnosi_widget = QWidget()
        diagnosi_layout = QVBoxLayout()
        diagnosi_widget.setLayout(diagnosi_layout)
        
        h = QHBoxLayout()
        lab = QLabel("IMPOSTAZIONI DEL TEST : ")
        lab.setObjectName("titoloi")
        
        self.tempo = QSpinBox(self)
        self.tempo.setRange(1, 15)
        self.tempo.setValue(1)
        self.tempo.setSingleStep(1)
        self.tempo.setMinimumWidth(100)
        
        tempolab = QLabel("minuti")
        tempolab.setObjectName("desc1")
        
        self.csv = QRadioButton("CSV")
        self.csv.setChecked(True)
        
        h.addWidget(lab)
        h.addStretch()
        h.addWidget(self.tempo)
        h.addWidget(tempolab)
        h.addStretch()
        h.addWidget(self.csv)
        h.addStretch()
        
        h2 = QHBoxLayout()
        
        self.start = QPushButton("START")
        self.start.setObjectName("big")
        self.start.clicked.connect(self.start_reg)
        self.stop = QPushButton("STOP")
        self.stop.setObjectName("bigd")
        self.stop.clicked.connect(self.stop_reg)
        
        labmi = QLabel("MISURE EFFETTUATE:")
        labmi.setObjectName("desc1")
        
        self.mi = QLabel("--")
        self.mi.setObjectName("pass")
        self.mi.setMinimumWidth(60)
        
        h2.addWidget(self.start)
        h2.addWidget(self.stop)
        h2.addStretch()
        h2.addWidget(labmi)
        h2.addWidget(self.mi)

        diagnosi_layout.addLayout(h)
        diagnosi_layout.addLayout(h2)
        diagnosi_layout.addStretch()
        
        self.stacked_widget.addWidget(diagnosi_widget)
        
    def start_reg(self):
        print("start")
        self.stop.setObjectName("big")
        self.start.setObjectName("bigd")

        self.start.style().unpolish(self.start)
        self.start.style().polish(self.start)
        self.start.update()

        self.stop.style().unpolish(self.stop)
        self.stop.style().polish(self.stop)
        self.stop.update()

        self.start.setEnabled(False)
        self.stop.setEnabled(True)

    def stop_reg(self):
        print("stop")
        self.stop.setObjectName("bigd")
        self.start.setObjectName("big")

        self.start.style().unpolish(self.start)
        self.start.style().polish(self.start)
        self.start.update()

        self.stop.style().unpolish(self.stop)
        self.stop.style().polish(self.stop)
        self.stop.update()

        self.start.setEnabled(True)
        self.stop.setEnabled(False)
        
    def show_diagnosi_page(self):
        self.stacked_widget.setCurrentIndex(1)
        self.master.contro_label(3)
        
    def home(self):
        self.stacked_widget.setCurrentIndex(0)
        self.master.contro_label(2)