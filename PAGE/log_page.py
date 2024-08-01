from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QPushButton, QScrollArea
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtCore import Qt
from OBJ import log_ogg as l 
from API import funzioni as f 

class LogPage(QWidget):
    def __init__(self, master):
        super().__init__()
        self.setWindowTitle("Log Page")
        
        self.master = master
        # Main Layout
        main_layout = QVBoxLayout()
        
        # Filters Layout
        filters_layout = QHBoxLayout()
        filters_layout.setContentsMargins(10, 10, 10, 10)
        filters_layout.setSpacing(15)
        
        # Filter by Date
        date_filter_layout = QVBoxLayout()
        date_label = QLabel("FILTRA PER DATA")
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_label.setObjectName("filterTitle")
        date_filter_layout.addWidget(date_label)
        
        date_inputs_layout1 = QHBoxLayout()
        date_inputs_layout1.addWidget(QLabel("DA"))
        self.ggd = QLineEdit()
        self.ggd.setMaximumWidth(60)
        date_inputs_layout1.addWidget(self.ggd)
        date_inputs_layout1.addWidget(QLabel("/"))
        self.mmd = QLineEdit()
        self.mmd.setMaximumWidth(60)
        date_inputs_layout1.addWidget(self.mmd)
        date_inputs_layout1.addWidget(QLabel("/"))
        self.aad = QLineEdit()
        self.aad.setMaximumWidth(120)
        date_inputs_layout1.addWidget(self.aad)
        date_filter_layout.addLayout(date_inputs_layout1)
        
        date_inputs_layout2 = QHBoxLayout()
        date_inputs_layout2.addWidget(QLabel("A "))
        self.gga = QLineEdit()
        self.gga.setMaximumWidth(60)
        date_inputs_layout2.addWidget(self.gga)
        date_inputs_layout2.addWidget(QLabel("/"))
        self.mma = QLineEdit()
        self.mma.setMaximumWidth(60)
        date_inputs_layout2.addWidget(self.mma)
        date_inputs_layout2.addWidget(QLabel("/"))
        self.aaa = QLineEdit()
        self.aaa.setMaximumWidth(120)
        date_inputs_layout2.addWidget(self.aaa)
        date_filter_layout.addLayout(date_inputs_layout2)
        
        date_filter_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        filters_layout.addLayout(date_filter_layout)
        filters_layout.addStretch()
        
        # Filter by Weight
        weight_filter_layout = QVBoxLayout()
        weight_label = QLabel("FILTRA PER PESO")
        weight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        weight_label.setObjectName("filterTitle")
        weight_filter_layout.addWidget(weight_label)
        
        weight_inputs_layout = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h1.addWidget(QLabel("DA"))
        self.pesod = QLineEdit()
        self.pesod.setMaximumWidth(150)
        h1.addWidget(self.pesod)
        h2.addWidget(QLabel("A"))
        self.pesoa = QLineEdit()
        self.pesoa.setMaximumWidth(150)
        h2.addWidget(self.pesoa)
        weight_inputs_layout.addLayout(h1)
        weight_inputs_layout.addLayout(h2)
        weight_filter_layout.addLayout(weight_inputs_layout)
        
        
        weight_filter_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        filters_layout.addLayout(weight_filter_layout)
        filters_layout.addStretch()
        
        # Filter by Priority
        priority_filter_layout = QVBoxLayout()
        priority_label = QLabel("FILTRA PER PRIORITÁ")
        priority_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        priority_label.setObjectName("filterTitle")
        priority_filter_layout.addWidget(priority_label)
        
        priority_buttons_layout = QVBoxLayout()
        test_radio = QCheckBox("test")
        test_radio.setChecked(True)
        intermedio_radio = QCheckBox("intermedio")
        intermedio_radio.setChecked(True)
        definitivo_radio = QCheckBox("definitivo")
        definitivo_radio.setChecked(True)
        
        priority_buttons_layout.addWidget(test_radio)
        priority_buttons_layout.addWidget(intermedio_radio)
        priority_buttons_layout.addWidget(definitivo_radio)
        priority_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        priority_filter_layout.addLayout(priority_buttons_layout)
        
        priority_filter_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        filters_layout.addLayout(priority_filter_layout)
        filters_layout.addStretch()
        
        # Filter Buttons
        filter_buttons_layout = QVBoxLayout()
        small_button = QPushButton("RIPRISTINA FILTRI")
        small_button.setObjectName("smallButton")
        small_button.setMaximumWidth(150)
        filter_buttons_layout.addWidget(small_button)
        
        large_button = QPushButton("CARICA FILTRI")
        large_button.setObjectName("largeButton")
        large_button.setMinimumWidth(250)
        filter_buttons_layout.addWidget(large_button)
        
        filters_layout.addLayout(filter_buttons_layout)
        
        main_layout.addLayout(filters_layout)
        
        # Scroll Area for Log Entries
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setObjectName("wid")
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Example Log Entries
        log_entries = [
            ("12 - 07 - 2024", "136,24", "DEFINTIVA", 2),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "TEST", 0),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "DEFINTIVA", 2),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "TEST", 0),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "DEFINTIVA", 2),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "TEST", 0),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "DEFINTIVA", 2),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "TEST", 0),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "DEFINTIVA", 2),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "TEST", 0),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "DEFINTIVA", 2),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "TEST", 0),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "DEFINTIVA", 2),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "TEST", 0),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "DEFINTIVA", 2),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "TEST", 0),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "DEFINTIVA", 2),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
            ("12 - 07 - 2024", "136,24", "TEST", 0),
            ("12 - 07 - 2024", "136,24", "INTERMEDIA", 1),
        ]
        
        for entry in log_entries:
            log_widget = l.LogEntryWidget(*entry)
            scroll_layout.addWidget(log_widget)
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        
        self.setLayout(main_layout)
        
        self.setAutoFillBackground(True)
        self.set_background_color()
        self.load_stylesheet()

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)

    def load_stylesheet(self):
        with open(f.get_style("log.qss"), "r") as file:
            self.setStyleSheet(file.read())