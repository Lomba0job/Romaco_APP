import sys
from PyQt6.QtCore import Qt, QFile, QTextStream, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QFrame, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar, 
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
        
        self.home_page()
        
        self.setLayout(self.main_layout)
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
    
    def home_page(self):
        p1 = p.ClickableWidget(f.get_img("DIAGNOSI.png"), "Misurazione Continua")
        p1.clicked.connect(self.diagnosi)
        
        p2 = p.ClickableWidget(f.get_img("PARAM_SET.png"), "Settaggio Parametri")
        
        p3 = p.ClickableWidget(f.get_img("DB_F.png"), "Fuzioni Database")
        
        p4 = p.ClickableWidget(f.get_img("LOG_DATA.png"), "Funzioni DataLog")
        
        p5 = p.ClickableWidget(f.get_img("MOD_IMPO.png"), "Funzioni Mod-Bus")
        
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch()
        self.main_layout.addWidget(p1)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(p2)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(p3)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(p4)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(p5)
        self.main_layout.addStretch()
        
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
                    
    def diagnosi(self):
        self.master.diagnosi_page()
        self.clearLayout(self.main_layout)
        
        
        l = QVBoxLayout()
        
        h = QHBoxLayout()
        lab = QLabel("IMPOSTAZIONI DEL TEST : ")
        lab.setObjectName("titoloi")
        
        self.tempo = QSpinBox(self)
        self.tempo.setRange(1, 15)  # Imposta il range minimo e massimo
        self.tempo.setValue(1)         # Imposta il valore iniziale
        self.tempo.setSingleStep(1)    # Imposta l'incremento per ogni passo
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

        
        l.addLayout(h)
        l.addLayout(h2)
        l.addStretch()
        
        self.main_layout.addLayout(l)

        
    def start_reg(self):
        print("start")
        self.stop.setObjectName("big")
        self.start.setObjectName("bigd")

        # Forza il ricaricamento dello stile
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

        # Forza il ricaricamento dello stile
        self.start.style().unpolish(self.start)
        self.start.style().polish(self.start)
        self.start.update()

        self.stop.style().unpolish(self.stop)
        self.stop.style().polish(self.stop)
        self.stop.update()

        self.start.setEnabled(True)
        self.stop.setEnabled(False)