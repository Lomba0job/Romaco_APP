from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QPushButton, QScrollArea
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
        filters_layout = QVBoxLayout()
        filters_layout.setContentsMargins(10, 10, 10, 10)
        filters_layout.setSpacing(15)
        
        # Filter by Date
        date_filter_layout = QVBoxLayout()
        date_label = QLabel("FILTRA PER DATA")
        date_label.setObjectName("filterTitle")
        date_filter_layout.addWidget(date_label)
        
        date_inputs_layout1 = QHBoxLayout()
        date_inputs_layout1.addWidget(QLabel("DA"))
        date_inputs_layout1.addWidget(QLineEdit())
        date_inputs_layout1.addWidget(QLabel("/"))
        date_inputs_layout1.addWidget(QLineEdit())
        date_inputs_layout1.addWidget(QLabel("/"))
        date_inputs_layout1.addWidget(QLineEdit())
        date_filter_layout.addLayout(date_inputs_layout1)
        
        date_inputs_layout2 = QHBoxLayout()
        date_inputs_layout2.addWidget(QLabel("A"))
        date_inputs_layout2.addWidget(QLineEdit())
        date_inputs_layout2.addWidget(QLabel("/"))
        date_inputs_layout2.addWidget(QLineEdit())
        date_inputs_layout2.addWidget(QLabel("/"))
        date_inputs_layout2.addWidget(QLineEdit())
        date_filter_layout.addLayout(date_inputs_layout2)
        
        filters_layout.addLayout(date_filter_layout)
        
        # Filter by Weight
        weight_filter_layout = QVBoxLayout()
        weight_label = QLabel("FILTRA PER PESO")
        weight_label.setObjectName("filterTitle")
        weight_filter_layout.addWidget(weight_label)
        
        weight_inputs_layout = QHBoxLayout()
        weight_inputs_layout.addWidget(QLabel("DA"))
        weight_inputs_layout.addWidget(QLineEdit())
        weight_inputs_layout.addWidget(QLabel("A"))
        weight_inputs_layout.addWidget(QLineEdit())
        weight_filter_layout.addLayout(weight_inputs_layout)
        
        filters_layout.addLayout(weight_filter_layout)
        
        # Filter by Priority
        priority_filter_layout = QVBoxLayout()
        priority_label = QLabel("FILTRA PER PRIORITÁ")
        priority_label.setObjectName("filterTitle")
        priority_filter_layout.addWidget(priority_label)
        
        priority_buttons_layout = QHBoxLayout()
        test_radio = QRadioButton("test")
        intermedio_radio = QRadioButton("intermedio")
        definitivo_radio = QRadioButton("definitivo")
        
        priority_buttons_layout.addWidget(test_radio)
        priority_buttons_layout.addWidget(intermedio_radio)
        priority_buttons_layout.addWidget(definitivo_radio)
        priority_filter_layout.addLayout(priority_buttons_layout)
        
        filters_layout.addLayout(priority_filter_layout)
        
        # Filter Buttons
        filter_buttons_layout = QVBoxLayout()
        small_button = QPushButton("RIPRISTINA FILTRI")
        small_button.setObjectName("smallButton")
        filter_buttons_layout.addWidget(small_button)
        
        large_button = QPushButton("CARICA FILTRI")
        large_button.setObjectName("largeButton")
        filter_buttons_layout.addWidget(large_button)
        
        filters_layout.addLayout(filter_buttons_layout)
        
        main_layout.addLayout(filters_layout)
        
        # Scroll Area for Log Entries
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Example Log Entries
        log_entries = [
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
        
        self.load_stylesheet()
        self.setLayout(main_layout)

    def load_stylesheet(self):
        with open(f.get_style("log.qss"), "r") as file:
            self.setStyleSheet(file.read())