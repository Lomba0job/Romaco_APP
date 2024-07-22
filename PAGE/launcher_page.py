from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFormLayout, QProgressBar
from PyQt6.QtCore import pyqtSignal, QThread, pyqtSlot
from pymodbus.client import ModbusSerialClient as ModbusClient
import serial.tools.list_ports
import sys
import glob
from API import Modbus as m
import time

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
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

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("Configurazione Modbus")
        layout.addWidget(label)

        form_layout = QFormLayout()

        self.port_combo = QComboBox()
        self.populate_ports()

        self.start_button = QPushButton("Start Scanning")
        self.start_button.clicked.connect(self.start_scanning)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate mode
        self.progress_bar.setVisible(False)

        form_layout.addRow("Port:", self.port_combo)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.start_button)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def populate_ports(self):
        ports = serial_ports()
        for port in ports:
            self.port_combo.addItem(port)

    def start_scanning(self):
        port = self.port_combo.currentText()
        self.scanner = ModbusScanner(port)
        self.scanner.result_ready.connect(self.scan_finished)
        self.scanner.start()
        self.progress_bar.setVisible(True)

    @pyqtSlot(list)
    def scan_finished(self, connected_ids):
        self.progress_bar.setVisible(False)
        
        if len(connected_ids) != 0:
            QMessageBox.information(self, "Scan Results", f"Connected IDs: {connected_ids}")
        else:
            QMessageBox.warning(self, "Scan Results", "No Connected ID")

        self.finished.emit()
