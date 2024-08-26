from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

from API import funzioni as f

class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.create_header()
    
    def create_header(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        logo_label = QLabel()
        ico = f.get_img("logo.jpg")
        logo_label.setPixmap(QPixmap(ico).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))   
        self.layout.addWidget(logo_label)

        self.title_label = QLabel("NANO<span style='color:#E74C3C'>LEVER</span>")
        self.title_label.setObjectName("title_label")
        self.layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("SISTEMA AD ISOLA")
        self.subtitle_label.setObjectName("subtitle_label")
        self.layout.addWidget(self.subtitle_label)

        self.layout.addStretch()
        
        self.configurazione_label = QLabel("IMPOSTAZIONI")
        self.configurazione_label.setObjectName("configurazione_label")
        self.layout.addWidget(self.configurazione_label)
    
    def update_header(self, title, subtitle, config_label):
        self.title_label.setText(title)
        self.subtitle_label.setText(subtitle)
        self.configurazione_label.setText(config_label)

    def add_back_button(self, callback):
        exit_button = QPushButton()
        logo_pixmap = QPixmap(f.get_img("back.png"))
        icon = QIcon(logo_pixmap)
        exit_button.setIcon(icon)
        exit_button.setIconSize(logo_pixmap.scaledToHeight(50).size())
        exit_button.setMaximumWidth(70)
        exit_button.clicked.connect(callback)
        self.layout.insertWidget(0, exit_button)