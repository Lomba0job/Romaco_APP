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

class Bilancia(QWidget):

    def __init__(self, numero_bilancia: int, screen_width, screen_height):
        super().__init__()
        
        self.setMaximumWidth(int(screen_width / 6.1))
        self.setMaximumHeight(int(screen_height * 0.5))
        layout = QVBoxLayout()
        
        print(numero_bilancia)
        #PRIMO LAYOUT 
        h0 = QHBoxLayout()
        h0.setSpacing(0)
        v0 = QVBoxLayout()
        
        logo_label = QLabel()
        ico = f.get_img("bilancia_chiara.png")
        larghezza = int(screen_width / 12)
        altezza = int(larghezza / 2)
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
        #layout.addStretch()
        
        #SECONDO LAYOUT 
        v1 = QVBoxLayout()
        v1.setSpacing(0)
        
        stato_adc = QLabel("STATO ADC: ")
        stato_adc.setObjectName("stato_label")
        self.stato_adc_valore = QLabel("OK")
        self.stato_adc_valore.setObjectName("stato_value")
        self.stato_adc_valore.setAlignment(Qt.AlignmentFlag.AlignRight)
        h1 = QHBoxLayout()
        h1.addWidget(stato_adc)
        h1.addWidget(self.stato_adc_valore)

        stato_elet = QLabel("STATO ELETTRONICA: ")
        stato_elet.setObjectName("stato_label")
        self.stato_elet_valore = QLabel("OK")
        self.stato_elet_valore.setObjectName("stato_value")
        self.stato_elet_valore.setAlignment(Qt.AlignmentFlag.AlignRight)
        h2 = QHBoxLayout()
        h2.addWidget(stato_elet)
        h2.addWidget(self.stato_elet_valore)

        stato_celle = QLabel("STATO CELLE: ")
        stato_celle.setObjectName("stato_label")
        self.stato_celle_valore = QLabel("OK")
        self.stato_celle_valore.setObjectName("stato_value")
        self.stato_celle_valore.setAlignment(Qt.AlignmentFlag.AlignRight)
        h3 = QHBoxLayout()
        h3.addWidget(stato_celle)
        h3.addWidget(self.stato_celle_valore)

        v1.addLayout(h1)
        v1.addLayout(h2)
        v1.addLayout(h3)
        
        layout.addLayout(v1)
        #layout.addStretch()
        
        #TERZO LAYOUT 
        tara_singola = QPushButton("TARA")
        tara_singola.setObjectName("tara")
        
        layout.addWidget(tara_singola)
        layout.setSpacing(int(screen_height * 0.05))
        
        
        #QUARTO LAYOUT 
        v3 = QVBoxLayout()
        v3.setSpacing(4)
        
        calib_label = QLabel("PESO DI CALIBRAZIONE")
        calib_label.setObjectName("stato_label")
        calib_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v3.addWidget(calib_label)
        
        h4 = QHBoxLayout()
        h4.setSpacing(0)
        
        self.peso_calib = QDoubleSpinBox(self)
        self.peso_calib.setRange(0.0, 100.0)  # Imposta il range minimo e massimo
        self.peso_calib.setDecimals(2)        # Imposta il numero di decimali
        self.peso_calib.setValue(5.00)         # Imposta il valore iniziale
        self.peso_calib.setSingleStep(0.1)    # Imposta l'incremento per ogni passo
        
        indice = QLabel("Kg")
        indice.setMaximumWidth(20)
        indice.setObjectName("indice")
        h4.addSpacing(10)
        h4.addWidget(self.peso_calib)
        h4.addWidget(indice)
        h4.addSpacing(10)
        v3.addLayout(h4)
        
        calib_singola = QPushButton("CALIBRAZIONE")
        calib_singola.setObjectName("calibrazione")
        v3.addWidget(calib_singola)
        
        layout.addLayout(v3)
        
        self.setLayout(layout)
        
        self.setAutoFillBackground(True)
        self.set_background_color()
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(254,254,254))
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
        
        
        
        