from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout
from PyQt6.QtCore import pyqtSignal
from pymodbus.client import ModbusSerialClient as ModbusClient

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

        self.port_edit = QLineEdit()
        self.baudrate_edit = QLineEdit()
        self.timeout_edit = QLineEdit()
        self.start_button = QPushButton("Start Scanning")
        self.start_button.clicked.connect(self.scan_modbus_network)

        form_layout.addRow("Port:", self.port_edit)
        form_layout.addRow("Baudrate:", self.baudrate_edit)
        form_layout.addRow("Timeout:", self.timeout_edit)
        layout.addLayout(form_layout)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def scan_modbus_network(self):
        port = self.port_edit.text()
        baudrate = int(self.baudrate_edit.text())
        timeout = int(self.timeout_edit.text())

        client = ModbusClient(method='rtu', port=port, baudrate=baudrate, timeout=timeout)
        client.connect()

        connected_ids = []
        for i in range(1, 247):
            response = client.read_coils(0, 1, unit=i)
            if not response.isError():
                connected_ids.append(i)

        client.close()

        QMessageBox.information(self, "Scan Results", f"Connected IDs: {connected_ids}")
        self.finished.emit()