from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from CMP import rectangle as r


class Home_Page(QWidget):

    def __init__(self, master):
        super().__init__()

        self.mast = master
        self.mast.setWindowTitle("HomePage")

        self.glWidget = None
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        # Left side layout
        left_layout = QVBoxLayout()
        
        self.config_label = QLabel("Scegli configurazione")
        left_layout.addWidget(self.config_label)
        
        self.combo_box = QComboBox()
        self.combo_box.addItems(["1", "2", "3", "4", "6"])
        left_layout.addWidget(self.combo_box)
        
        self.num_label = QLabel("Numero bilance")
        left_layout.addWidget(self.num_label)
        
        self.load_button = QPushButton("Carica configurazione")
        self.load_button.clicked.connect(self.loadConfiguration)
        left_layout.addWidget(self.load_button)
        
        main_layout.addLayout(left_layout)
        
        # Right side fixed area
        self.fixed_area = QWidget()
        self.fixed_area.setFixedSize(int(self.mast.width() * 0.45), int(self.mast.height() * 0.8))
        self.fixed_area.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        palette = self.fixed_area.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('white'))
        self.fixed_area.setPalette(palette)
        self.fixed_area.setAutoFillBackground(True)
        
        main_layout.addWidget(self.fixed_area, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(main_layout)

    def loadConfiguration(self):
        num_rectangles = int(self.combo_box.currentText())
        
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