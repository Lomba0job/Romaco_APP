from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QRadioButton, QTextEdit, QHBoxLayout,QSpacerItem , QSizePolicy, 
    QGridLayout, QFrame, QLineEdit
)
from PyQt6.QtGui import QPixmap, QColor, QFont
from PyQt6.QtCore import Qt, pyqtSignal
import locale
from datetime import datetime


from API import funzioni as f, API_db as db, LOG as l 

class SalvaPesoWidget(QWidget):
    peso_salvato = pyqtSignal()  # Signal emitted when the weight is saved

    def __init__(self, master):
        super().__init__()
        
        self.master = master
        self.preUI()
        self.setAutoFillBackground(True)
        self.set_background_color()
        self.load_stylesheet()

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)

    def preUI(self):
        self.main_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap(f.get_img("logo.jpg"))
        logo_label.setPixmap(logo_pixmap.scaledToHeight(50))
        header_layout.addWidget(logo_label)

        title_label = QLabel("NANO<span style='color:#E74C3C'>LEVER</span>")
        title_label.setObjectName("title_label")
        header_layout.addWidget(title_label)

        subtitle_label = QLabel("SISTEMA AD ISOLA")
        subtitle_label.setObjectName("subtitle_label")
        header_layout.addWidget(subtitle_label)

        header_layout.addStretch()
        
        configurazione_label = QLabel("CONFIGURAZIONE")
        configurazione_label.setObjectName("configurazione_label")
        header_layout.addWidget(configurazione_label)

        wid = QWidget()
        wid.setMaximumHeight(70)
        wid.setObjectName("menulab")
        wid.setLayout(header_layout)
        self.main_layout.addWidget(wid)

        # Content Grid
        grid_layout = QGridLayout()

        # Total Weight
        total_weight_label = QLabel("PESO TOTALE RILEVATO:")
        total_weight_label.setObjectName("label")
        grid_layout.addWidget(total_weight_label, 0, 0, 1, 3)

        total_weight_value = QLabel("0")
        total_weight_value.setObjectName("value")
        grid_layout.addWidget(total_weight_value, 0, 4, 1, 5)

        # Configuration info
        # config_label = QLabel("DERIVATO DA UNA CONFIGURAZIONE A:")
        # config_label.setObjectName("label")
        # grid_layout.addWidget(config_label, 0, 2)

        # config_value = QLabel("4 BILANCE")
        # config_value.setObjectName("value")
        # grid_layout.addWidget(config_value, 0, 3)

        # date_label = QLabel("IN DATA:")
        # date_label.setObjectName("label")
        # grid_layout.addWidget(date_label, 1, 2)

        # date_value = QLabel("31 luglio 2024")
        # date_value.setObjectName("value")
        # grid_layout.addWidget(date_value, 1, 3)

        # Individual scale weights
        scales_label = QLabel("PESO RILEVATO PER BILANCIA:")
        scales_label.setObjectName("label")
        grid_layout.addWidget(scales_label, 3, 0, 1, 3)

        for i in range(6):
            v = QVBoxLayout()
            v.setSpacing(5)
            peso_bil = "0"
            scale_label = QLabel(f"BILANCIA {i+1}")
            scale_label.setObjectName("scale_label")
            scale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scale_label.setMaximumHeight(40)
            if peso_bil != None:
                scale_value = QLabel(peso_bil)
            else: 
                scale_value = QLabel("NC")
            scale_value.setObjectName("scale_value")
            scale_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scale_value.setMaximumHeight(40)
            
            v.addWidget(scale_label)
            v.addWidget(scale_value)
            
            
            grid_layout.addLayout(v, 3, (i*3)+4, 1, 2, Qt.AlignmentFlag.AlignLeft)
        inner = QLabel("")
        inner.setMinimumHeight(40)
        
        
        grid_layout.addWidget(inner, 6, 3)
        
        grid_layout.addWidget(inner, 4, 0)
        grid_layout.addWidget(inner, 7, 0)
        grid_layout.addWidget(inner, 10, 0)
        # Machine front
        front_label = QLabel("SIGLA MACCHINA:")
        front_label.setObjectName("label")
        grid_layout.addWidget(front_label, 6, 0, 1, 3)

        front_combo = QLineEdit()
        grid_layout.addWidget(front_combo, 6, 4, 1, 4)

        # Description
        description_label = QLabel("DESCRIZIONE PESATA:")
        description_label.setObjectName("label")
        grid_layout.addWidget(description_label, 8, 0, 1, 3)

        description_input = QTextEdit()
        grid_layout.addWidget(description_input, 8, 4, 2, 17)

        # Priority
        priority_label = QLabel("PRIORITÁ PESATA:")
        priority_label.setObjectName("label")
        grid_layout.addWidget(priority_label, 11, 0, 1, 3)

        priority_layout = QHBoxLayout()
        test_radio = QRadioButton("TEST")
        intermediate_radio = QRadioButton("INTERMEDIA")
        intermediate_radio.setChecked(True)
        definitive_radio = QRadioButton("DEFINITIVA")

        priority_layout.addWidget(test_radio)
        priority_layout.addStretch()
        priority_layout.addWidget(intermediate_radio)
        priority_layout.addStretch()
        priority_layout.addWidget(definitive_radio)
        

        grid_layout.addLayout(priority_layout, 11, 4, 1, 17)
        h = QHBoxLayout()
        h.addSpacing(20)
        h.addLayout(grid_layout)
        h.addSpacing(20)
        
        self.main_layout.addLayout(h)
        self.main_layout.addSpacing(50)
        # Action buttons
        button_layout = QHBoxLayout()
        delete_button = QPushButton("ELIMINA")
        delete_button.setObjectName("delete_button")
        delete_button.clicked.connect(self.back)
        
        save_button = QPushButton("SALVA")
        save_button.setObjectName("save_button")
        save_button.clicked.connect(self.save)

        button_layout.addWidget(delete_button)
        button_layout.addSpacing(int(self.master.screen_width * 0.4))
        button_layout.addWidget(save_button)

        self.main_layout.addLayout(button_layout)
        self.setLayout(self.main_layout)

    
    def initUI(self, peso, b1, b2=None, b3=None, b4=None, b5=None, b6=None):
        self.clearLayout(self.main_layout)

        peso = str(peso / 1000)
        self.peso_tot = peso
        
        b1 = str(b1/1000)
        self.peso_b1 = b1
        
        if b2 != None: 
            b2 = str(b2/1000)
            self.peso_b2 = b2 
        else:
            self.peso_b2 = 0.0
            
        if b3 != None: 
            b3 = str(b3/1000)
            self.peso_b3 = b3 
        else:
            self.peso_b3 = 0.0
            
        if b4 != None: 
            b4 = str(b4/1000)
            self.peso_b4 = b4 
        else:
            self.peso_b4 = 0.0
            
        if b5 != None: 
            b5 = str(b5/1000)
            self.peso_b5 = b5
        else:
            self.peso_b5 = 0.0
            
        if b6 != None: 
            b6 = str(b6/1000)
            self.peso_b6 = b6
        else:
            self.peso_b6 = 0.0
        
        # Header
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap(f.get_img("logo.jpg"))
        logo_label.setPixmap(logo_pixmap.scaledToHeight(50))
        header_layout.addWidget(logo_label)

        title_label = QLabel("NANO<span style='color:#E74C3C'>LEVER</span>")
        title_label.setObjectName("title_label")
        header_layout.addWidget(title_label)

        subtitle_label = QLabel("SISTEMA AD ISOLA")
        subtitle_label.setObjectName("subtitle_label")
        header_layout.addWidget(subtitle_label)

        header_layout.addStretch()
        
        configurazione_label = QLabel("CONFIGURAZIONE")
        configurazione_label.setObjectName("configurazione_label")
        header_layout.addWidget(configurazione_label)

        wid = QWidget()
        wid.setMaximumHeight(70)
        wid.setObjectName("menulab")
        wid.setLayout(header_layout)
        self.main_layout.addWidget(wid)

        # Content Grid
        grid_layout = QGridLayout()

        # Total Weight
        total_weight_label = QLabel("PESO TOTALE RILEVATO:")
        total_weight_label.setObjectName("label")
        grid_layout.addWidget(total_weight_label, 0, 0, 1, 3)

        total_weight_value = QLabel(peso)
        total_weight_value.setObjectName("value")
        grid_layout.addWidget(total_weight_value, 0, 4, 1, 5)

        # Configuration info
        # config_label = QLabel("DERIVATO DA UNA CONFIGURAZIONE A:")
        # config_label.setObjectName("label")
        # grid_layout.addWidget(config_label, 0, 2)

        # config_value = QLabel("4 BILANCE")
        # config_value.setObjectName("value")
        # grid_layout.addWidget(config_value, 0, 3)

        # date_label = QLabel("IN DATA:")
        # date_label.setObjectName("label")
        # grid_layout.addWidget(date_label, 1, 2)

        # date_value = QLabel("31 luglio 2024")
        # date_value.setObjectName("value")
        # grid_layout.addWidget(date_value, 1, 3)

        # Individual scale weights
        scales_label = QLabel("PESO RILEVATO PER BILANCIA:")
        scales_label.setObjectName("label")
        grid_layout.addWidget(scales_label, 3, 0, 1, 3)

        for i in range(6):
            v = QVBoxLayout()
            v.setSpacing(5)
            if i == 0:
                peso_bil = b1
            if i == 1:
                peso_bil = b2
            if i == 2:
                peso_bil = b3
            if i == 3:
                peso_bil = b4
            if i == 4:
                peso_bil = b5
            if i == 5:
                peso_bil = b6
            scale_label = QLabel(f"BILANCIA {i+1}")
            scale_label.setObjectName("scale_label")
            scale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scale_label.setMaximumHeight(40)
            if peso_bil != None:
                scale_value = QLabel(peso_bil)
            else: 
                scale_value = QLabel("NC")
            scale_value.setObjectName("scale_value")
            scale_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
            scale_value.setMaximumHeight(40)
            
            v.addWidget(scale_label)
            v.addWidget(scale_value)
            
            
            grid_layout.addLayout(v, 3, (i*3)+4, 1, 2, Qt.AlignmentFlag.AlignLeft)
        inner = QLabel("")
        inner.setMinimumHeight(40)
        
        
        grid_layout.addWidget(inner, 6, 3)
        
        grid_layout.addWidget(inner, 4, 0)
        grid_layout.addWidget(inner, 7, 0)
        grid_layout.addWidget(inner, 10, 0)
        # Machine front
        front_label = QLabel("SIGLA MACCHINA:")
        front_label.setObjectName("label")
        grid_layout.addWidget(front_label, 6, 0, 1, 3)

        self.front_combo = QLineEdit()
        grid_layout.addWidget(self.front_combo, 6, 4, 1, 4)

        # Description
        description_label = QLabel("DESCRIZIONE PESATA:")
        description_label.setObjectName("label")
        grid_layout.addWidget(description_label, 8, 0, 1, 3)

        self.description_input = QTextEdit()
        grid_layout.addWidget(self.description_input, 8, 4, 2, 17)

        # Priority
        priority_label = QLabel("PRIORITÁ PESATA:")
        priority_label.setObjectName("label")
        grid_layout.addWidget(priority_label, 11, 0, 1, 3)

        priority_layout = QHBoxLayout()
        self.test_radio = QRadioButton("TEST")
        self.intermediate_radio = QRadioButton("INTERMEDIA")
        self.intermediate_radio.setChecked(True)
        self.definitive_radio = QRadioButton("DEFINITIVA")

        priority_layout.addWidget(self.test_radio)
        priority_layout.addStretch()
        priority_layout.addWidget(self.intermediate_radio)
        priority_layout.addStretch()
        priority_layout.addWidget(self.definitive_radio)
        

        grid_layout.addLayout(priority_layout, 11, 4, 1, 17)
        h = QHBoxLayout()
        h.addSpacing(20)
        h.addLayout(grid_layout)
        h.addSpacing(20)
        
        self.main_layout.addLayout(h)
        self.main_layout.addSpacing(50)
        # Action buttons
        button_layout = QHBoxLayout()
        delete_button = QPushButton("ELIMINA")
        delete_button.setObjectName("delete_button")
        delete_button.clicked.connect(self.back)
        
        save_button = QPushButton("SALVA")
        save_button.setObjectName("save_button")
        save_button.clicked.connect(self.save)

        button_layout.addWidget(delete_button)
        button_layout.addSpacing(int(self.master.screen_width * 0.4))
        button_layout.addWidget(save_button)

        self.main_layout.addLayout(button_layout)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    
    def save(self):
        l.log_file(107)
        nome = self.front_combo.text()
        decs = self.description_input.toPlainText()
        stato = 0
        if self.test_radio.isChecked():
            stato = 0
        elif self.intermediate_radio.isChecked():
            stato = 1
        elif self.definitive_radio.isChecked():
            stato = 2
            
        # Ottieni la data odierna
        oggi = datetime.now()

        # Formatala secondo la lingua di sistema
        data_formattata = oggi.strftime('%d-%m-%Y')

        # print("Data odierna:", data_formattata)

        self.peso_tot, self.peso_b1, self.peso_b2, self.peso_b3, self.peso_b4, self.peso_b5, self.peso_b6, nome, decs, stato, data_formattata
        ris = db.put(peso_tot=self.peso_tot, b1=self.peso_b1, b2=self.peso_b2, b3=self.peso_b3, b4=self.peso_b4, b5=self.peso_b5, b6=self.peso_b6, desc=decs, prio=stato, data=data_formattata, nome=nome)
        if ris == 1:
            l.log_file(408)
        else:
            l.log_file(7)
            self.master.change_page(1) 
            self.master.navbar.setVisible(True)
            self.peso_salvato.emit()
        
    def back(self):
        self.master.change_page(1)
        self.master.navbar.setVisible(True)
        
        
    def load_stylesheet(self):
        with open(f.get_style("salva_peso.qss"), "r") as file:
            self.setStyleSheet(file.read())