import concurrent.futures
import threading
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy, QProgressBar
from PyQt6.QtCore import Qt, QFile, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QSize
from PyQt6.QtGui import QColor, QPalette
import time 

from CMP import rectangle as r, loading2 as carica
from API import funzioni as f, modbus_generico as mb
from OBJ import thread_pesata as t


class Home_Page(QWidget):

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("HomePage")
        
        self.glWidget = None
        self.main_layout = None
        self.left_layout = None
        self.config_label = None
        self.pesata_thread = None  # Per tenere il riferimento al thread
        self.progress_bar = None  # Per tenere il riferimento alla barra di progresso
        self.timer = None  # Timer per aggiornare la barra di progresso
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
        self._log_thread_info("initUI")
        # Pulisci i widget esistenti dai layout
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
        # Rimuovi il widget precedente e il suo layout se esistono
        if self.glWidget is not None:
            self.fixed_area.layout().removeWidget(self.glWidget)
            self.glWidget.deleteLater()

        # Crea e aggiungi il nuovo widget
        self.glWidget = r.VTKWidget(num_rectangles=num_rectangles)
        self.glWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Pulisci qualsiasi layout esistente nell'area fissa
        if self.fixed_area.layout() is not None:
            old_layout = self.fixed_area.layout()
            QWidget().setLayout(old_layout)

        layout = QHBoxLayout()
        layout.addWidget(self.glWidget)

        self.fixed_area.setLayout(layout)
        self.fixed_area.setAutoFillBackground(False)


    def pesata(self):
        
        self._log_thread_info("pesata")
        # Pulisci l'UI esistente
        self.clearLayout(self.left_layout)

        # Crea una barra di progresso animata\
        h0 = QHBoxLayout()
        
        self.progress_bar = carica.QCustom3CirclesLoader(size=200)
        testo = QLabel("CARICAMENTO")
        testo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        testo.setObjectName("titolo")

        h0.addStretch()
        h0.addWidget(self.progress_bar)
        h0.addStretch()
        self.left_layout.addStretch()
        self.left_layout.addLayout(h0)
        self.left_layout.addSpacing(30)
        self.left_layout.addWidget(testo)
        self.left_layout.addStretch()

       
        # Avvia il thread
        self.pesata_thread = t.PesataThread(self.master)
        self.pesata_thread.pesata_completata.connect(self.on_pesata_completata)
        self.pesata_thread.start()



    @pyqtSlot(list)
    def on_pesata_completata(self, pesi_bilance):
        
        self._log_thread_info("on_pesata_completata")
        # Ferma il thread e la barra di progresso
        self.pesata_thread.quit()
        #self.progress_bar.hide()
        self.clearLayout(self.left_layout)
        print(pesi_bilance)
        
        if len(pesi_bilance) != 0 and len(pesi_bilance) == len(self.master.lista_bilance):  
            # Visualizza l'UI finale con i risultati della pesata
            self.finalUI(pesi_bilance)
        else: 
            self.initUI()

    def salva_f(self):
        self.master.save_call(self.pesoTotale, self.peso_bilance)

    def _log_thread_info(self, function_name):
        """Log thread information for diagnostics."""
        current_thread = threading.current_thread()
        print(f"DEBUG THREAD | {function_name} eseguito su thread: {current_thread.name} (ID: {current_thread.ident})")