from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFormLayout, QProgressBar, QHBoxLayout, QGroupBox, QGraphicsEffect
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot, QFile, QTextStream, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt6.QtGui import QFontDatabase, QPixmap, QPalette, QColor
import serial.tools.list_ports
import sys
import glob
from API import modbus_generico as m
from API import funzioni as f
import time
from API import LOG as l
from OBJ import bilancia as b



def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
            l.log_file(108)
        except (OSError, serial.SerialException):
            #l.log_file(410)
            pass
    return result

class OrdinamentoWorker(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, lista_bilance):
        super().__init__()
        self.lista_bilance: list[b.Bilancia] = lista_bilance

    def run(self):
        status_ok = [0 for _ in range(len(self.lista_bilance))]

        while 0 in status_ok:
            for i in range(len(self.lista_bilance)):
                if status_ok[i] == 0:
                    try:
                        result = self.lista_bilance[i].check_coil_status()
                        if result == 1:
                            status_ok[i] = 1
                            self.lista_bilance[i].set_number(sum(status_ok))
                        self.progress_updated.emit(sum(status_ok))
                            
                    except Exception as e:
                        l.log_file(411, f"{self.lista_bilance[i].modbusI.address}: {e}")
            time.sleep(0.2)
        
        self.finished.emit()
        

class ModbusScanner(QThread):
    result_ready = pyqtSignal(list)

    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        connected_ids = m.scan_modbus_network(self.port)
        self.result_ready.emit(connected_ids)

class LauncherWidget(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setAutoFillBackground(True)
        self.set_background_color()
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241,241,241))
        self.setPalette(p)

    def initUI(self):
        self.setWindowTitle("Configurazione NANOLEVER")
        
        main_layout = QVBoxLayout()

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
        wid.setObjectName("menulab")
        wid.setLayout(header_layout)
        main_layout.addWidget(wid)

        # Content
        content_layout = QHBoxLayout()
        content_layout.addSpacing(100)
        # Left side - Controls
        h0 = QHBoxLayout()
        controls_layout = QVBoxLayout()
        controls_layout.addStretch()
        detect_button = QPushButton("RILEVARE LE PORTE DISPONIBILI")
        detect_button.clicked.connect(self.rileva_porte)
        detect_button.setMaximumWidth(400)
        h0.addStretch()
        h0.addWidget(detect_button)
        h0.addStretch()
        
        controls_layout.addLayout(h0)
        controls_layout.addSpacing(60)
        h1 = QHBoxLayout()
        
        porta_label = QLabel("PORTA SELEZIONATA")
        porta_label.setMinimumWidth(200)
        porta_label.setObjectName("passo1")
        h1.addWidget(porta_label)

        self.port_combo = QComboBox()
        self.port_combo.setObjectName("combo")
        self.port_combo.setMinimumWidth(400)
        h1.addWidget(self.port_combo)
        controls_layout.addLayout(h1)
        controls_layout.addSpacing(100)

        self.start_button = QPushButton("AVVIARE CONFIGURAZIONE AUTOMATICA")
        self.start_button.setMaximumWidth(600)
        self.start_button.setMinimumHeight(70)
        self.start_button.clicked.connect(self.start_scanning)

        controls_layout.addStretch()
        self.label = QLabel("")
        self.label.setVisible(False)
        self.label.setObjectName("desc")
        
        
        content_layout.addLayout(controls_layout)

        # Right side - Usage steps
        usage_widget = QWidget()
        usage_widget.setObjectName("wid")
        usage_layout = QVBoxLayout(usage_widget)

        fasi_label = QLabel("FASI DI UTILIZZO")
        fasi_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fasi_label.setObjectName("t_wid")
        usage_layout.addStretch(1)
        usage_layout.addWidget(fasi_label)
        usage_layout.addStretch(2)

        steps = [
            "Collegare le bilance tramite il cavo in dotazione.",
            "Collegare la prima bilancia al PC.",
            "Posizionare le bilance seguendo uno ordine circolare\npartendo da quella collegata al PC.",
            "Rimuovere eventuali componenti dalla superficie della\nbilancia.",
            "Identificare e selezionare la porta della bilancia.",
            "Avviare la configurazione automatica."
        ]

        for i, step in enumerate(steps, 1):
            step_layout = QHBoxLayout()
            step_number = QLabel(f"PASSO {i}:")
            step_number.setMaximumWidth(300)
            step_number.setObjectName("passo")
            
            step_desc = QLabel(step)
            step_desc.setAlignment(Qt.AlignmentFlag.AlignLeft)
            # step_desc.setAlignment(Qt.AlignmentFlag.AlignBottom)
            step_desc.setObjectName("desc")
            step_layout.addSpacing(100)
            step_layout.addWidget(step_number)
            step_layout.addWidget(step_desc)
            step_layout.addStretch()
            usage_layout.addLayout(step_layout)
            usage_layout.addSpacing(20)
        
        usage_layout.addStretch(2)
        content_layout.addStretch()
        content_layout.addWidget(usage_widget)
        content_layout.addSpacing(40)
        main_layout.addLayout(content_layout)
        usage_widget.setMinimumHeight(600)
        usage_widget.setMaximumHeight(600)
        usage_widget.setMinimumWidth(700)
        usage_widget.setMaximumWidth(700)
        
        h2 = QHBoxLayout()
        h2.addStretch()
        h2.addWidget(self.start_button)
        h2.addStretch()
        
        main_layout.addLayout(h2)
        main_layout.addSpacing(50)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.progress_bar)

        self.setLayout(main_layout)

        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("launcher.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)

    def start_scanning(self):
        self.progress_bar.setVisible(True)
        self.label.setVisible(True)
        self.label.setText("Identificazione bilance")
        self.progress_bar.setRange(0, 0)
        
        port = self.port_combo.currentText()
        self.scanner = ModbusScanner(port)
        self.scanner.result_ready.connect(self.scan_finished)
        self.scanner.start()
        
        self.start_button.setVisible(False)
        
    def rileva_porte(self):
        result = serial_ports()
        for port in result:
            self.port_combo.addItem(port)
            
        
    @pyqtSlot(list)
    def scan_finished(self, connected_ids):
        self.progress_bar.setRange(0, 1000)  # Determinate mode
        self.label.setVisible(True)
        if len(connected_ids) != 0:
            self.lista_bilance = m.configure(self.port_combo.currentText(), connected_ids)
            if self.lista_bilance is not None:
                self.ordinamento()
            else:
                QMessageBox.warning(self, "Scan Results", "Errore 402")
                self.start_button.setVisible(True)
                self.label.setVisible(False)
                self.progress_bar.setVisible(False)
        else:
            QMessageBox.warning(self, "Scan Results", "Errore 401")
            self.start_button.setVisible(True)
            self.label.setVisible(False)
            self.progress_bar.setVisible(False)

    def ordinamento(self):
        l.log_file(8)
        self.worker = OrdinamentoWorker(self.lista_bilance)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.start_ordinamento()

    def start_ordinamento(self):
        self.worker.start()

    def update_progress(self, value):
        # Assuming each bilancia corresponds to an equal percentage of the progress bar
        # print(value)
        # print(len(self.lista_bilance))
        percentage = (value / len(self.lista_bilance)) * 1000
        next_percentage =  (value+1 / len(self.lista_bilance)) * 1000
        soglia = (1 /len(self.lista_bilance) * 1000) / 3
        
        if value == 0:
            self.label.setText(f"Ordinamento bilance (Ricerca della bilancia collegata per prima)")
        elif value == 1:
            self.label.setText(f"Ordinamento bilance (Ricerca della bilancia collegata per seconda)")
        elif value == 2:
            self.label.setText(f"Ordinamento bilance (Ricerca della bilancia collegata per terza)")
        elif value == 3:
            self.label.setText(f"Ordinamento bilance (Ricerca della bilancia collegata per quarta)")
        elif value == 4:
            self.label.setText(f"Ordinamento bilance (Ricerca della bilancia collegata per quinta)")
        elif value == 5:
            self.label.setText(f"Ordinamento bilance (Ricerca della bilancia collegata per sesta)")
            
            
        # print(f"DEBUG PROGRESSBAR | percentage: {percentage}, value: {self.progress_bar.value()}, next_percentage: {next_percentage}. ")
        if(int(percentage) <= self.progress_bar.value()):
            if self.progress_bar.value()+1 < int(next_percentage):
                if(int(next_percentage) - self.progress_bar.value()) > int(soglia): 
                    self.progress_bar.setValue(int(self.progress_bar.value()+5))
                else: 
                    self.progress_bar.setValue(int(self.progress_bar.value()+1))
        else:
            self.progress_bar.setValue(int(percentage))

    def on_finished(self):
        l.log_file(1, f' ordinamento {len(self.lista_bilance)}')
        #QMessageBox.information(self, "Ordinamento", "Ordinamento completato")
        self.finished.emit()
        self.start_button.setVisible(True)
        self.start_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.label.setVisible(False)
