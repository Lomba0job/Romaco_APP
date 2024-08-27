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
        
        
        self.main_layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        
        self.home_page() #indice 0
        self.log_page() #indice 1
        self.db_page()  #indice 2
        
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)
        
        
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
        
        home_widget = QWidget()
        home_layout = QHBoxLayout()
        home_widget.setLayout(home_layout)
        
        p1 = p.ClickableWidget(f.get_img("DB_F.png"),     "Operazioni Database") 
        p1.clicked.connect(self.db_operatione)
        p2 = p.ClickableWidget(f.get_img("LOG_DATA.png"), "Operazioni DataLog") 
        p2.clicked.connect(self.dataLog_operatione)
        
        home_layout.addStretch()
        home_layout.addWidget(p1)
        home_layout.addSpacing(50)
        home_layout.addWidget(p2)
        home_layout.addStretch()
        
        self.stacked_widget.addWidget(home_widget)
        
    def db_page(self):
        
        home_widget = QWidget()
        home_layout = QHBoxLayout()
        home_widget.setLayout(home_layout)
        
        p1 = p.ClickableWidget(f.get_img("trash.png"),     "Elimina dati database") 
        p2 = p.ClickableWidget(f.get_img("share.png"), "Esporta dati database") 
        
        home_layout.addStretch()
        home_layout.addWidget(p1)
        home_layout.addSpacing(50)
        home_layout.addWidget(p2)
        home_layout.addStretch()
        
        self.stacked_widget.addWidget(home_widget)
        
    def log_page(self):
        
        home_widget = QWidget()
        home_layout = QHBoxLayout()
        home_widget.setLayout(home_layout)
        
        p1 = p.ClickableWidget(f.get_img("trash.png"), "Elimina DataLog") 
        p2 = p.ClickableWidget(f.get_img("share.png"), "Esporta DataLog") 
        
        home_layout.addStretch()
        home_layout.addWidget(p1)
        home_layout.addSpacing(50)
        home_layout.addWidget(p2)
        home_layout.addStretch()
        
        self.stacked_widget.addWidget(home_widget)
         
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
        self.stacked_widget.setCurrentIndex(0)
        self.master.contro_label(1)
    
    
    def dataLog_operatione(self):
        self.stacked_widget.setCurrentIndex(1)
        self.master.contro_label(4)
    
    
    def db_operatione(self):
        self.stacked_widget.setCurrentIndex(2)
        self.master.contro_label(5)
    