from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFormLayout, QProgressBar, QHBoxLayout, QGroupBox, QGraphicsEffect
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot, QFile, QTextStream, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt6.QtGui import QFontDatabase, QPixmap, QPalette, QColor
from pymodbus.client import ModbusSerialClient as ModbusClient
import serial.tools.list_ports
import sys
import glob
from API import funzioni as f
import time
from CMP import Bilancia_diagno as b, Bilancia_diagno_deactive as bd

class DiagnosticWidget(QWidget):

   
    def __init__(self, master):
        super().__init__()
        self.master = master
        # Set the window title
        self.setWindowTitle("Diagnostica")
        self.setWindowTitle("RESPONSE ANALYZE APP")
        
        self.screen_width =  self.master.screen_width 
        self.screen_height = self.master.screen_height

        
        # Set the central widget
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        v1 = QVBoxLayout()

        # Create and add 6 instances of Home_Page
        for i in range(1, 7):
            if i < len(self.master.lista_bilance):
                home_page = b.Bilancia(i, self.screen_width-10, self.screen_height-10, self.master.lista_bilance[i-1])
                home_page.setObjectName("weed")
            else:
                home_page = bd.Bilancia(i, self.screen_width-10, self.screen_height-10)
                home_page.setObjectName("weed")
                
            raggruppa = QWidget()
            l0 = QHBoxLayout()
            l0.setSpacing(0)
            l0.addWidget(home_page)
            l0.setContentsMargins(2,2,2,2)
            raggruppa.setLayout(l0)
            
            
            raggruppa.setObjectName("bil")
            raggruppa.setContentsMargins(1,1,1,1)
            
            main_layout.addWidget(raggruppa)
            
            
        self.setStyleSheet("""
            QWidget#bil{
                border: 1px solid grey;
                border-radius: 9px;
            }
        """)
            
        v1.addStretch()
        v1.setContentsMargins(0,0,0,0)
        v1.addLayout(main_layout)
        v1.addSpacing(10)
        
        self.setLayout(v1)
        self.setAutoFillBackground(True)
        self.set_background_color()
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241,241,241))
        self.setPalette(p)
        # Load the stylesheet