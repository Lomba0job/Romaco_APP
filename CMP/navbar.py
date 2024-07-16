import sys
from PyQt6.QtCore import Qt, QFile, QTextStream, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QFrame, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar
)
from PyQt6.QtGui import QPixmap, QAction, QIcon
import os 

# from risorse import resources_rc
from API import funzioni as f
class NavbarWidget(QFrame):
    settings_button_clicked = pyqtSignal()

    def __init__(self, parent=None):
        
        
        
        super().__init__(parent)
        self.setObjectName("navbar")
        self.setFixedHeight(60)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(20)

        # Logo
        logo_label = QLabel()
        
        ico = f.get_img("logo.jpg")
        logo_label.setPixmap(QPixmap(ico).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(logo_label)
        
        # Company Name
        name_label = QLabel("NANO")
        name_label.setObjectName("companyName")
        name_label2 = QLabel("LEVER")
        name_label2.setObjectName("companyName2")
        wid = QWidget()
        l = QHBoxLayout()
        l.setSpacing(0)  # Imposta lo spazio tra i widget a 0
        l.addWidget(name_label)
        l.addWidget(name_label2)
        wid.setLayout(l)
        layout.addWidget(wid)

        # Spacer
        spacer_left = QFrame()
        spacer_left.setFrameShape(QFrame.Shape.NoFrame)
        spacer_left.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(spacer_left)

        # Navigation Buttons
        self.home_button = QPushButton("HOMEPAGE")
        self.home_button.setObjectName("navButton")

        
        self.home_button.setProperty('active', False)
        
        self.home_button.setFixedSize(100, 50)
        
        layout.addWidget(self.home_button)
  
        
        # Spacer
        spacer_right = QFrame()
        spacer_right.setFrameShape(QFrame.Shape.NoFrame)
        spacer_right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(spacer_right)
        
        # Vertical Line
        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.Shape.VLine)
        vertical_line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(vertical_line)
        
        # Settings Icon
        settings_button = QPushButton()
        settings_button.setIcon(QIcon(f.get_img("settings.png")))
        settings_button.setIconSize(QSize(24, 24))
        settings_button.setFixedSize(50, 50)
        layout.addWidget(settings_button)

        settings_button.clicked.connect(self.settings_button_clicked.emit)

        self.setLayout(layout)

        file = QFile(f.get_style("navbar.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)
