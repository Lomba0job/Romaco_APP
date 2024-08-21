import sys
from PyQt6.QtCore import Qt, QFile, QTextStream, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QFrame, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar, 
    QDoubleSpinBox
    
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