from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QPushButton, QScrollArea
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtCore import Qt
from OBJ import log_ogg as l 
from API import funzioni as f
from API import API_db as db, LOG as log  # Importa le funzioni del database

class LogPage(QWidget):
    def __init__(self, master):
        super().__init__()
        self.setWindowTitle("Log Page")
        
        self.master = master
        self.page_number = 1  # Inizia dalla prima pagina
        
        # Main Layout
        main_layout = QVBoxLayout()
        
        """
        v 2.0 ricerca filtrata
        # Filters Layout
        filters_layout = QHBoxLayout()
        filters_layout.setContentsMargins(10, 10, 10, 10)
        filters_layout.setSpacing(15)
        
        # (Resto del codice per la creazione del layout dei filtri...)
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
        self.test_radio = QCheckBox("test")
        self.test_radio.setChecked(True)
        self.intermedio_radio = QCheckBox("intermedio")
        self.intermedio_radio.setChecked(True)
        self.definitivo_radio = QCheckBox("definitivo")
        self.definitivo_radio.setChecked(True)
        
        priority_buttons_layout.addWidget(self.test_radio)
        priority_buttons_layout.addWidget(self.intermedio_radio)
        priority_buttons_layout.addWidget(self.definitivo_radio)
        priority_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        priority_filter_layout.addLayout(priority_buttons_layout)
        
        priority_filter_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        filters_layout.addLayout(priority_filter_layout)
        filters_layout.addStretch()

        # Filter Buttons
        filter_buttons_layout = QVBoxLayout()
        reset_button = QPushButton("RIPRISTINA FILTRI")
        reset_button.setObjectName("smallButton")
        reset_button.setMaximumWidth(150)
        reset_button.clicked.connect(self.reset_filters)  # Aggiungi azione per il reset
        filter_buttons_layout.addWidget(reset_button)
        
        apply_button = QPushButton("CARICA FILTRI")
        apply_button.setObjectName("largeButton")
        apply_button.setMinimumWidth(250)
        apply_button.clicked.connect(self.load_filtered_data)  # Aggiungi azione per caricare i dati
        filter_buttons_layout.addWidget(apply_button)
        
        filters_layout.addLayout(filter_buttons_layout)
        
        main_layout.addLayout(filters_layout)
        
        """
        # Scroll Area for Log Entries
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("wid")
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll_area)
        
        self.setLayout(main_layout)
        
        self.setAutoFillBackground(True)
        self.set_background_color()
        self.load_stylesheet()

        self.load_data()  # Carica i dati iniziali dal database

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)

    def load_stylesheet(self):
        with open(f.get_style("log.qss"), "r") as file:
            self.setStyleSheet(file.read())

    def load_data(self):
        log.log_file(111)
        log_entries = db.get_latest_entries()  # Recupera i dati dal database
        # print(log_entries)
        self.populate_log_entries(log_entries)
        
    def load_filtered_data(self):
        # Qui applichi i filtri e carichi i dati filtrati dal database
        date_from = f"{self.aad.text()}-{self.mmd.text()}-{self.ggd.text()}"
        date_to = f"{self.aaa.text()}-{self.mma.text()}-{self.gga.text()}"
        priority = None  # Aggiungi logica per filtrare per priorità, se necessario
        
        # Usa la logica di filtraggio che preferisci, per esempio:
        log_entries = db.get_filtered(self.page_number, date_from, date_to, priority)
        self.populate_log_entries(log_entries)
        
    def populate_log_entries(self, log_entries):
        # Rimuove i vecchi widget
        for i in reversed(range(self.scroll_layout.count())): 
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Aggiunge i nuovi widget
        for entry in log_entries:
            date_str = str(entry['data'])  # Converti il valore di data in una stringa
            # print(f"Creating LogEntryWidget with date: {date_str}, peso_totale: {entry['peso_totale']}, name: {entry['name']}, priority: {entry['priority']}")
           
            log_widget = l.LogEntryWidget(date=date_str, peso_totale=entry['peso_totale'], name=entry['name'], priority=entry['priority'])
            self.scroll_layout.addWidget(log_widget)
            
    # def reset_filters(self):
        # Resetta tutti i campi dei filtri
        # self.ggd.clear()
        # self.mmd.clear()
        # self.aad.clear()
        # self.gga.clear()
        # self.mma.clear()
        # self.aaa.clear()
        # self.pesod.clear()
        # self.pesoa.clear()
        # Carica tutti i dati dal database
        # self.load_data()
        # 
    # def load_filtered_data(self):
        # Qui applichi i filtri e carichi i dati filtrati dal database
        # date_from = f"{self.aad.text()}-{self.mmd.text()}-{self.ggd.text()}"
        # date_to = f"{self.aaa.text()}-{self.mma.text()}-{self.gga.text()}"
        # 
        # Filtra per priorità
        # priority = []
        # if self.test_radio.isChecked():
            # priority.append(0)  # Priorità TEST
        # if self.intermedio_radio.isChecked():
            # priority.append(1)  # Priorità INTERMEDIO
        # if self.definitivo_radio.isChecked():
            # priority.append(2)  # Priorità DEFINITIVO
# 
        # Usa la logica di filtraggio per ottenere i dati dal database
        # log_entries = db.get_filtered(self.page_number, date_from, date_to, priority)
        # self.populate_log_entries(log_entries)