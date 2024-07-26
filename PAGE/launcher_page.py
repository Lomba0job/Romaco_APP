from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFormLayout, QProgressBar, QHBoxLayout, QGroupBox
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot, QFile, QTextStream
from PyQt6.QtGui import QFontDatabase, QPixmap, QPalette, QColor    
from pymodbus.client import ModbusSerialClient as ModbusClient
import serial.tools.list_ports
import sys
import glob
from API import modbus_generico as m
from API import funzioni as f
import time



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
        except (OSError, serial.SerialException):
            pass
    return result

class OrdinamentoWorker(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, lista_bilance):
        super().__init__()
        self.lista_bilance = lista_bilance

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
                        print(f"Errore durante l'elaborazione della Bilancia {self.lista_bilance[i].modbusI.address}: {e}")
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
        p.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(p)

    def initUI(self):
        self.setWindowTitle("Luancher page")

        
        
        main_layout = QVBoxLayout()

        # Horizontal layout for the title and logo
        title_layout = QHBoxLayout()

        # Add the logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(f.get_img("logo.jpg"))  # Path to your logo file
        logo_label.setPixmap(logo_pixmap.scaledToHeight(50))
        title_layout.addWidget(logo_label)

        # Add the title and subtitle
        title_label = QLabel("NANO<span style='color:#E74C3C'>LEVER</span>")
        title_label.setObjectName("title_label")
        title_layout.addWidget(title_label)

        subtitle_label = QLabel("SISTEMA AD ISOLA")
        subtitle_label.setObjectName("subtitle_label")
        title_layout.addWidget(subtitle_label)

        title_layout.addStretch()
        main_layout.addLayout(title_layout)

        # Horizontal layout for the main content
        content_layout = QHBoxLayout()

        # Left vertical layout for the controls
        controls_layout = QVBoxLayout()

        # Form layout for port selection
        form_layout = QFormLayout()
        self.port_combo = QComboBox()
        self.populate_ports()
        form_layout.addRow("Porta Selezionata", self.port_combo)
        controls_layout.addLayout(form_layout)

        self.detect_button = QPushButton("Rileva le porte disponibili")
        self.detect_button.clicked.connect(self.populate_ports)
        controls_layout.addWidget(self.detect_button)

        self.start_button = QPushButton("Avvia Configurazione Automatica")
        self.start_button.clicked.connect(self.start_scanning)
        controls_layout.addWidget(self.start_button)

        controls_layout.addStretch()
        content_layout.addLayout(controls_layout)

        # Right vertical layout for the usage steps and progress
        wid = QWidget()
        wid.setObjectName("wid")
        usage_layout = QVBoxLayout()

        
        
        titolo_wid = QLabel(" ISTRUZIONI DI UTILIZZO ")
        titolo_wid.setObjectName("t_wid")
        titolo_wid.setMinimumHeight(200)
        
        l0 = QHBoxLayout()
        p0 = QLabel("PASSO 1:")
        p0.setObjectName("passo")
        d0 = QLabel("Collegare le bilance tramite il cavo in dotazione. ")
        d0.setObjectName("desc")
        l0.addWidget(p0)
        l0.addWidget(d0)
        
        
        l1 = QHBoxLayout()
        p1 = QLabel("PASSO 2:")
        p1.setObjectName("passo")
        d1 = QLabel("Collegare la prima bilancia al PC.")
        d1.setObjectName("desc")
        l1.addWidget(p1)
        l1.addWidget(d1)
        
        l2 = QHBoxLayout()
        p2 = QLabel("PASSO 3:")
        p2.setObjectName("passo")
        d2 = QLabel("Posizionare le bilance seguendo uno ordine circolare\npartendo da quella collegata al PC.")
        d2.setObjectName("desc")
        l2.addWidget(p2)
        l2.addWidget(d2)
        
        l3 = QHBoxLayout()
        p3 = QLabel("PASSO 4:")
        p3.setObjectName("passo")
        d3 = QLabel("Rimuovere eventuali componenti dalla superficie della\nbilancia. ")
        d3.setObjectName("desc")
        l3.addWidget(p3)
        l3.addWidget(d3)
        
        l4 = QHBoxLayout()
        p4 = QLabel("PASSO 5:")
        p4.setObjectName("passo")
        d4 = QLabel("Identificare e selezionare la porta della bilancia. ")
        d4.setObjectName("desc")
        l4.addWidget(p4)
        l4.addWidget(d4)
        
        l5 = QHBoxLayout()
        p5 = QLabel("PASSO 6:")
        p5.setObjectName("passo")
        d5 = QLabel(" Avviare la configurazione automatica.")
        d5.setObjectName("desc")
        l5.addWidget(p5)
        l5.addWidget(d5)
        

        
        
        usage_layout.setSpacing(2)
        
        usage_layout.addWidget(titolo_wid)
        usage_layout.addLayout(l0)
        usage_layout.addLayout(l1)
        usage_layout.addLayout(l2)
        usage_layout.addLayout(l3)
        usage_layout.addLayout(l4)
        usage_layout.addLayout(l5)
        
        
        
        
        
        
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        
        wid.setLayout(usage_layout)
        content_layout.addWidget(wid)
        content_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(content_layout)
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

    def populate_ports(self):
        ports = serial_ports()
        self.port_combo.clear()
        for port in ports:
            self.port_combo.addItem(port)

    def start_scanning(self):
        port = self.port_combo.currentText()
        self.scanner = ModbusScanner(port)
        self.scanner.result_ready.connect(self.scan_finished)
        self.scanner.start()
        self.start_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate mode

    @pyqtSlot(list)
    def scan_finished(self, connected_ids):
        self.progress_bar.setRange(0, 100)  # Determinate mode
        if len(connected_ids) != 0:
            self.lista_bilance = m.configure(self.port_combo.currentText(), connected_ids)
            self.ordinamento()
        else:
            QMessageBox.warning(self, "Scan Results", "No Connected ID")
            self.start_button.setEnabled(True)
            self.progress_bar.setVisible(False)

    def ordinamento(self):
        self.worker = OrdinamentoWorker(self.lista_bilance)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.start_ordinamento()

    def start_ordinamento(self):
        self.worker.start()

    def update_progress(self, value):
        percentage = (value / len(self.lista_bilance)) * 100
        self.progress_bar.setValue(int(percentage))

    def on_finished(self):
        QMessageBox.information(self, "Ordinamento", "Ordinamento completato")
        self.finished.emit()
        self.start_button.setEnabled(True)
