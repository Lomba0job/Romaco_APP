import sys
from PyQt6.QtCore import Qt, QFile, QTextStream, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QFrame, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar, 
    QDoubleSpinBox
    
)
from PyQt6.QtGui import QPixmap, QAction, QIcon, QColor
import os 

from CMP import rectangle as r
from API import funzioni as f

class Bilancia_deactive(QWidget):

    def __init__(self, numero_bilancia: int, screen_width):
        super().__init__()
        
        layout = QVBoxLayout()
        
        
        #PRIMO LAYOUT 
        h0 = QHBoxLayout()
        v0 = QHBoxLayout()
        
        logo_label = QLabel()
        ico = f.get_img("logo.jpg")
        larghezza = screen_width / 12
        altezza = larghezza / 2
        logo_label.setPixmap(QPixmap(ico).scaled(larghezza, altezza, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        h0.addWidget(logo_label)
        
        numero = QLabel(str(numero_bilancia))
        numero.setObjectName("numero")
        bilancia = QLabel("BILANCIA")
        bilancia.setObjectName("bilancia")
        
        numero.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v0.addWidget(numero)
        bilancia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v0.addWidget(bilancia)
        
        h0.addLayout(v0)
        
        layout.addLayout(h0)
        layout.addStretch()
        
        #SECONDO LAYOUT 
        deactive = QLabel("NON COLLEGATA")
        deactive.setObjectName("no")
        
        layout.addWidget(deactive)
        layout.addStretch()
        
        #TERZO LAYOUT 
        tara_singola = QPushButton("TARA")
        tara_singola.setObjectName("tara")
        
        layout.addWidget(tara_singola)
        layout.setSpacing(70)
        
        v3 = QVBoxLayout()
        
        calib_label = QLabel("PESO DI CALIBRAZIONE")
        calib_label.setObjectName("stato_label")
        v3.addWidget(calib_label)
        
        h4 = QHBoxLayout()
        self.peso_calib = QDoubleSpinBox(self)
        self.peso_calib.setRange(0.0, 100.0)  # Imposta il range minimo e massimo
        self.peso_calib.setDecimals(2)        # Imposta il numero di decimali
        self.peso_calib.setValue(5.00)         # Imposta il valore iniziale
        self.peso_calib.setSingleStep(0.1)    # Imposta l'incremento per ogni passo
        
        indice = QLabel("Kg")
        indice.setObjectName("indice")
        h4.addWidget(self.peso_calib)
        h4.addWidget(indice)
        v3.addLayout(h4)
        
        calib_singola = QPushButton("CALIBRAZIONE")
        calib_singola.setObjectName("calibrazione")
        v3.addWidget(calib_singola)
        
        layout.addLayout(v3)
            
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241,241,241))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("bilancia.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)
        
        
        
        
        
        
        
        