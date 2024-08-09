from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy, QProgressBar
from PyQt6.QtCore import Qt, QFile, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QColor, QPalette


from CMP import rectangle as r
from API import funzioni as f, modbus_generico as mb

class PesataThread(QThread):
    pesata_completata = pyqtSignal(list)  # Signal to emit when the pesata is completed

    def __init__(self, master):
        super().__init__()
        self.master = master

    def run(self):
        QThread.msleep(500)  # Aspetta 500 millisecondi prima di iniziare il ciclo di pesatura
        
        pesi_bilance = []
        print(f"DEBUG PESATA | bilance {len(self.master.lista_bilance)}")
        for b in self.master.lista_bilance:
            pesotot = mb.get_totWeight(b.modbusI)
            print(f"DEBUG PESATA | peso TOT {pesotot} {b.modbusI.address}")
            if pesotot != -1:
                peso = mb.get_cellWeight(b.modbusI)
                print(f"DEBUG PESATA check | pesi {peso}")
                s = peso[0]
                print(f"DEBUG PESATA check | pesi {peso}, primo {s}")
                warn = False
                for p in peso: 
                    if abs(p-s) > 20000:  # SOTTOCHIAVE IMPOSTAZIONE 
                        warn = True  # ! AGGIUNGERE ERRORE
                print(f"DEBUG PESATA check | war {warn}")
                if not warn:
                    pesi_bilance.append(pesotot)
        if len(pesi_bilance) != 0 and len(pesi_bilance) == len(self.master.lista_bilance):  
            self.pesata_completata.emit(pesi_bilance)  # Emit the signal with the result

class Home_Page(QWidget):

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("HomePage")
        
        self.glWidget = None
        self.main_layout = None
        self.left_layout = None
        self.config_label = None
        self.pesata_thread = None  # To hold the reference to the thread
        self.progress_bar = None  # To hold the reference to the progress bar
        self.timer = None  # Timer for updating the progress bar
        self.preUI()
        self.setAutoFillBackground(True)
        self.set_background_color()
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241,241,241))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("home.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)

    
    def preUI(self):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        
        push_config = QPushButton()
        push_config.setText("ESEGUI LA CONFIGURAZIONE")
        push_config.setObjectName("puls")
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
        self.load_stylesheet()

    def reinitUI(self):
        self.clearLayout(self.left_layout)
        self.clearLayout(self.fixed_area.layout())

        # Ricrea il contenuto di left_layout senza ricreare il layout stesso
        push_config = QPushButton()
        push_config.setText("ESEGUI LA CONFIGURAZIONE")
        push_config.setObjectName("puls")
        push_config.clicked.connect(self.master.launcher_call)
        self.left_layout.addStretch()
        self.left_layout.addWidget(push_config)
        self.left_layout.addStretch()

        # Reutilizza la fixed_area esistente
        self.fixed_area.setFixedSize(int(self.master.width() * 0.45), int(self.master.height() * 0.8))
        self.fixed_area.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        palette = self.fixed_area.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('white'))
        self.fixed_area.setPalette(palette)
        self.fixed_area.setAutoFillBackground(True)

        self.main_layout.addWidget(self.fixed_area, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.load_stylesheet()
        
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def initUI(self):
        # Clear existing widgets from layouts
        self.clearLayout(self.left_layout)
        self.clearLayout(self.fixed_area.layout())
        self.glWidget = None
        print(f"DEBUG HOMEPAGE {len(self.master.lista_bilance)}")
        numero = len(self.master.lista_bilance)
        
        h1 = QHBoxLayout()
        self.config_label = QLabel(f"Rilevata configurazione da {numero} bilance")
        self.config_label.setObjectName("desc")
        push_config = QPushButton()
        push_config.setText("RIESEGUI LA CONFIGURAZIONE")
        push_config.setObjectName("small")
        push_config.clicked.connect(self.master.launcher_call)
        h1.addWidget(self.config_label)
        h1.addWidget(push_config)
        
        
        push_weught = QPushButton()
        push_weught.setText("ESEGUI UNA PESATA")
        push_weught.setObjectName("puls")
        push_weught.clicked.connect(self.pesata)
        
        self.left_layout.addLayout(h1)
        self.left_layout.addStretch()
        self.left_layout.addWidget(push_weught)
        self.left_layout.addStretch()
        self.load_stylesheet()

        if numero != 0:
            self.loadConfiguration()
            
    def finalUI(self, lista_pesi):
        self.clearLayout(self.left_layout)
        
        numero = len(self.master.lista_bilance)
        h1 = QHBoxLayout()
        self.config_label = QLabel(f"Rilevata configurazione da {numero} bilance")
        self.config_label.setObjectName("desc")
        push_config = QPushButton()
        push_config.setText("RIESEGUI LA CONFIGURAZIONE")
        push_config.setObjectName("small")
        push_config.clicked.connect(self.master.launcher_call)
        h1.addWidget(self.config_label)
        h1.addWidget(push_config)
        
        
        titolo = QLabel("PESO TOTALE RILEVATO: ")
        titolo.setObjectName("titolo")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pes = 0
        for peso in lista_pesi:
            pes += peso
        peso_v = str(pes / 1000) + " Kg"
        peso = QLabel(peso_v)
        peso.setObjectName("peso")
        peso.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        v = QVBoxLayout()
        for i in range(numero):
            h = QHBoxLayout()
            numbi = QLabel(f"PESO BILANCIA {i+1}:")
            numbi.setObjectName("passo")
            numbi.setMinimumWidth(200)
            numbi.setMaximumWidth(200)
            print(f"DEBUG | Pesata {i}, {lista_pesi}")
            peso_v = str(lista_pesi[i] / 1000) + " Kg"
            pesobi = QLabel(peso_v)
            pesobi.setObjectName("desc1")
            pesobi.setMinimumWidth(60)
            
            h.addSpacing(50)
            h.addWidget(numbi)
            h.addSpacing(10)
            h.addWidget(pesobi)
            h.addStretch()
            
            v.addLayout(h)
        
        h2 = QHBoxLayout()
        salva = QPushButton()
        salva.setText("SALVA PESATA")
        salva.setObjectName("puls")
        salva.clicked.connect(self.salva_f)
        riesegui = QPushButton()
        riesegui.setText("ESEGUI PESATA")
        riesegui.setObjectName("puls")
        riesegui.clicked.connect(self.pesata)
        
        h2.addWidget(salva)
        h2.addStretch()
        h2.addWidget(riesegui)
                
        self.left_layout.addLayout(h1)
        self.left_layout.addSpacing(int(self.master.screen_height * 0.2))
        self.left_layout.addWidget(titolo)
        self.left_layout.addWidget(peso)
        self.left_layout.addSpacing(int(self.master.screen_height * 0.1))
        self.left_layout.addLayout(v)
        self.left_layout.addStretch()
        self.left_layout.addLayout(h2)
        self.left_layout.addSpacing(int(self.master.screen_height * 0.05))
        self.load_stylesheet()
        
        self.pesoTotale = pes
        self.peso_bilance = lista_pesi


    
    def loadConfiguration(self):
        num_rectangles = len(self.master.lista_bilance) 
        for b in self.master.lista_bilance:
            print(f"{b.position} corrisponde all'id {b.modbusI.address}")     
        # Remove the previous widget and its layout if they exist
        if self.glWidget is not None:
            self.fixed_area.layout().removeWidget(self.glWidget)
            self.glWidget.deleteLater()
        
        # Create and add the new widget
        self.glWidget = r.VTKWidget(num_rectangles=num_rectangles)
        
        # Clear any existing layout in the fixed area
        if self.fixed_area.layout() is not None:
            old_layout = self.fixed_area.layout()
            QWidget().setLayout(old_layout)
        
        layout = QHBoxLayout()
        layout.addWidget(self.glWidget)
        
        self.fixed_area.setLayout(layout)
        self.fixed_area.setAutoFillBackground(False)
        
        
    def pesata(self):
        # Clear the existing UI
        self.clearLayout(self.left_layout)

        # Create a bouncing progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Range 0, 0 makes it an infinite progress bar
        self.progress_bar.setTextVisible(False)
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.progress_bar)
        self.left_layout.addStretch()

        # Start the thread
        self.pesata_thread = PesataThread(self.master)
        self.pesata_thread.pesata_completata.connect(self.on_pesata_completata)
        self.pesata_thread.start()

    @pyqtSlot(list)
    def on_pesata_completata(self, pesi_bilance):
        # Stop the thread and the progress bar
        self.pesata_thread.quit()
        self.progress_bar.hide()
        self.left_layout.removeWidget(self.progress_bar)

        # Display the final UI with the pesata results
        self.finalUI(pesi_bilance)
        
    def salva_f(self):
        self.master.save_call(self.pesoTotale, self.peso_bilance)