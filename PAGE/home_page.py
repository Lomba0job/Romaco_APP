from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from CMP import rectangle as r


class Home_Page(QWidget):

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("HomePage")

        self.glWidget = None
        self.main_layout = None
        self.left_layout = None
        self.config_label = None
        self.preUI()
    
    def preUI(self):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        
        push_config = QPushButton()
        push_config.setText("ESEGUI LA CONFIGURAZIONE")
        push_config.clicked.connect(self.master.launcher_call)
        self.left_layout.addStretch()
        self.left_layout.addWidget(push_config)
        self.left_layout.addStretch()
        self.main_layout.addLayout(self.left_layout)
        
        # Right side fixed area
        self.fixed_area = QWidget()
        self.fixed_area.setFixedSize(int(self.master.width() * 0.45), int(self.master.height() * 0.8))
        self.fixed_area.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        palette = self.fixed_area.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('white'))
        self.fixed_area.setPalette(palette)
        self.fixed_area.setAutoFillBackground(True)
        
        self.main_layout.addWidget(self.fixed_area, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(self.main_layout)

    def initUI(self):
        # Clear existing widgets from layouts
        self.clearLayout(self.left_layout)
        self.clearLayout(self.fixed_area.layout())

        print(f"DEBUG HOMEPAGE {len(self.master.lista_bilance)}")
        numero = len(self.master.lista_bilance)
        self.config_label = QLabel(f"CONFIGURAZIONE DA {numero} BILANCE")
        self.left_layout.addWidget(self.config_label)
        
        if numero != 0:
            self.loadConfiguration()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def loadConfiguration(self):
        num_rectangles = len(self.master.lista_bilance) 
        for b in self.master.lista_bilance:
            print(f"{b.position} corrisponde all'id {b.modbusI.address}")     
        # Remove the previous widget and its layout if they exist
        if self.glWidget is not None:
            self.fixed_area.layout().removeWidget(self.glWidget)
            self.glWidget.deleteLater()
        
        # Create and add the new widget
        self.glWidget = r.GLWidget(num_rectangles=num_rectangles)
        
        # Clear any existing layout in the fixed area
        if self.fixed_area.layout() is not None:
            old_layout = self.fixed_area.layout()
            QWidget().setLayout(old_layout)
        
        layout = QHBoxLayout()
        layout.addWidget(self.glWidget)
        
        self.fixed_area.setLayout(layout)
        self.fixed_area.setAutoFillBackground(False)