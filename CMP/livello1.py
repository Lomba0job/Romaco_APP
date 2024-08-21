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

from CMP import puls_livello1 as p 

class Livello1(QWidget):

    def __init__(self, master):
        super().__init__()
        self.master:s.Settings = master
        
        
        self.main_layout = QHBoxLayout()
        
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
        p1 = p.ClickableWidget(f.get_img("DB_F.png"),     "Operazioni Database") 
        p2 = p.ClickableWidget(f.get_img("LOG_DATA.png"), "Operazioni DataLog") 
        
        self.main_layout.addStretch()
        self.main_layout.addWidget(p1)
        self.main_layout.addSpacing(50)
        self.main_layout.addWidget(p2)
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
                    
    def home(self):
        pass