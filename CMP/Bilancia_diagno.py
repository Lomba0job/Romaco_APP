import sys
import threading
from PyQt6.QtCore import Qt, QFile, QTextStream, QSize, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QFrame, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar, 
    QDoubleSpinBox
)
from PyQt6.QtGui import QPixmap, QAction, QIcon, QColor
import os 
import time 

from OBJ import bilancia as b
from API import funzioni as f, modbus_generico as mg, LOG as l 

class Bilancia(QWidget):

    adc_status_signal = pyqtSignal(int)
    cells_status_signal = pyqtSignal(int)
    tara_completata_signal = pyqtSignal(int)
    calibrazione_completata_signal = pyqtSignal(int)
    adc = False
    ele = False
    celle = False
    elettronica = True

    def __init__(self, numero_bilancia: int, screen_width, screen_height, bilancia: b.Bilancia):
        super().__init__()
        self.trigger_warning = False
        self.setMaximumWidth(int(screen_width / 6.1))
        self.setMaximumHeight(int(screen_height * 0.5))
        layout = QVBoxLayout()

        self.numero = numero_bilancia
        print(numero_bilancia)
        self.bilancia = bilancia

        # Signals connections
        self.adc_status_signal.connect(self.update_adc_status_ui)
        self.cells_status_signal.connect(self.update_cells_status_ui)
        self.tara_completata_signal.connect(self.update_tara_ui)
        self.calibrazione_completata_signal.connect(self.update_calibrazione_ui)

        # PRIMO LAYOUT 
        h0 = QHBoxLayout()
        h0.setSpacing(0)
        v0 = QVBoxLayout()

        logo_label = QLabel()
        ico = f.get_img("bilancia_chiara.png")
        larghezza = int(screen_width / 12)
        altezza = int(larghezza / 2)
        logo_label.setPixmap(QPixmap(ico).scaled(larghezza, altezza, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        h0.addWidget(logo_label)

        numero = QLabel(str(numero_bilancia))
        numero.setObjectName("numero")
        bilancia = QLabel("BILANCIA")
        bilancia.setObjectName("bilancia")

        numero.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v0.addWidget(numero)
        bilancia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v0.addWidget(bilancia)

        h0.addLayout(v0)

        layout.addLayout(h0)
        # layout.addStretch()

        # SECONDO LAYOUT 
        v1 = QVBoxLayout()
        v1.setSpacing(0)

        stato_adc = QLabel("STATO ADC: ")
        stato_adc.setObjectName("stato_label")
        self.stato_adc_valore = QLabel("OK")
        self.stato_adc_valore.setObjectName("stato_value_ok")
        self.stato_adc_valore.setAlignment(Qt.AlignmentFlag.AlignRight)
        h1 = QHBoxLayout()
        h1.addWidget(stato_adc)
        h1.addWidget(self.stato_adc_valore)

        stato_elet = QLabel("STATO ELETTRONICA: ")
        stato_elet.setObjectName("stato_label")
        self.stato_elet_valore = QLabel("OK")
        self.stato_elet_valore.setObjectName("stato_value_ok")
        self.stato_elet_valore.setAlignment(Qt.AlignmentFlag.AlignRight)
        h2 = QHBoxLayout()
        h2.addWidget(stato_elet)
        h2.addWidget(self.stato_elet_valore)

        stato_celle = QLabel("STATO CELLE: ")
        stato_celle.setObjectName("stato_label")
        self.stato_celle_valore = QLabel("OK")
        self.stato_celle_valore.setObjectName("stato_value_ok")
        self.stato_celle_valore.setAlignment(Qt.AlignmentFlag.AlignRight)
        h3 = QHBoxLayout()
        h3.addWidget(stato_celle)
        h3.addWidget(self.stato_celle_valore)

        v1.addLayout(h1)
        v1.addLayout(h2)
        v1.addLayout(h3)

        layout.addLayout(v1)
        # layout.addStretch()

        # TERZO LAYOUT 
        tara_singola = QPushButton("TARA")
        tara_singola.setObjectName("tara")
        tara_singola.clicked.connect(self.effettua_tara)

        layout.addWidget(tara_singola)
        layout.setSpacing(int(screen_height * 0.05))

        # QUARTO LAYOUT 
        v3 = QVBoxLayout()
        v3.setSpacing(4)

        calib_label = QLabel("PESO DI CALIBRAZIONE")
        calib_label.setObjectName("stato_label")
        calib_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v3.addWidget(calib_label)

        h4 = QHBoxLayout()
        h4.setSpacing(0)

        self.peso_calib = QDoubleSpinBox(self)
        self.peso_calib.setRange(0.0, 100.0)  # Imposta il range minimo e massimo
        self.peso_calib.setDecimals(2)        # Imposta il numero di decimali
        self.peso_calib.setValue(5.00)         # Imposta il valore iniziale
        self.peso_calib.setSingleStep(0.1)    # Imposta l'incremento per ogni passo

        indice = QLabel("Kg")
        indice.setMaximumWidth(25)
        indice.setObjectName("indice")
        h4.addSpacing(10)
        h4.addWidget(self.peso_calib)
        h4.addWidget(indice)
        h4.addSpacing(10)
        v3.addLayout(h4)

        calib_singola = QPushButton("CALIBRAZIONE")
        calib_singola.setObjectName("calibrazione")
        calib_singola.clicked.connect(self.effettua_calibrazione)
        v3.addWidget(calib_singola)

        layout.addLayout(v3)

        self.setLayout(layout)

        self.setAutoFillBackground(True)
        self.set_background_color()

    def laod_status(self, adc, elettronica, celle):
        if adc: 
            self.stato_adc_valore.setText("OK")
            self.stato_adc_valore.setObjectName("stato_value_ok")
        else:
            self.stato_adc_valore.setText("NOT OK")
            self.stato_adc_valore.setObjectName("stato_value_not")
            
        if elettronica: 
            self.stato_elet_valore.setText("OK")
            self.stato_elet_valore.setObjectName("stato_value_ok")
        else:
            self.stato_elet_valore.setText("NOT OK")
            self.stato_elet_valore.setObjectName("stato_value_not")
            
        if celle: 
            self.stato_celle_valore.setText("OK")
            self.stato_celle_valore.setObjectName("stato_value_ok")
        else:
            self.stato_celle_valore.setText("NOT OK")
            self.stato_celle_valore.setObjectName("stato_value_not")
        self.load_stylesheet()
        
    def get_status(self):
        adc = self.stato_adc_valore.text() == "OK"
        ele = self.stato_elet_valore.text() == "OK"
        cell = self.stato_celle_valore.text() == "OK"
        return adc, ele, cell
            
    def update(self):
        ele = True
        future_adc = mg.get_adcs_status(self.bilancia.modbusI)
        if future_adc is not None:
            future_adc.add_done_callback(self.handle_adc_status)
        else:
            l.log_file(702, "ERROR UPDATE | Future for get_adcs_status is None")
    
        future_cells = mg.get_cells_status(self.bilancia.modbusI)
        if future_cells is not None:
            future_cells.add_done_callback(self.handle_cells_status)
        else:
            l.log_file(702, "ERROR UPDATE | Future for get_cells_status is None")
    
    def handle_adc_status(self, future):
        self._log_thread_info("handle_adc_status")
        try:
            ris = future.result()
            self.adc_status_signal.emit(ris)
        except Exception as e:
            l.log_file(702, f"Errore durante l'aggiornamento dello stato ADC: {e}")

    def update_adc_status_ui(self, ris):
        self._log_thread_info("update_adc_status_ui")
        if ris == 0: 
            self.adc = True
        else: 
            self.adc = False
            self.ele = False
        self.update_status()
    
    def handle_cells_status(self, future):
        self._log_thread_info("handle_cells_status")
        try:
            ris = future.result()
            self.cells_status_signal.emit(ris)
        except Exception as e:
            l.log_file(702, "Errore durante l'aggiornamento dello stato delle celle: {e}")
    
    def update_cells_status_ui(self, ris):
        self._log_thread_info("update_cells_status_ui")
        if ris == 0: 
            self.celle = True
        else: 
            self.celle = False
            self.ele = False
        self.update_status()
    
    def update_status(self):
        self._log_thread_info("update_status")
        if not self.celle and not self.adc: 
            self.ele = False
        else:
            self.ele = True
        adc_v, ele_v, cel_v = self.get_status()
        if self.adc != adc_v or self.ele != ele_v or self.celle != cel_v:
            # print(f"DEBUG UPDATE | adc{self.adc}, ele{self.ele}, celle{self.celle}")
            self.laod_status(self.adc, self.ele, self.celle)
        if not self.ele:
            # print(f"DEBUG UPDATE | elettronica False")
            if self.elettronica:
                self.elettronica_false_since = time.time()
                self.elettronica = False
            self.check_ele()
        else:
            self.elettronica = True
            self.elettronica_false_since = None
            self.trigger_warning = False
    
    def check_ele(self):
        self._log_thread_info("check_ele")
        if self.elettronica_false_since is not None:
            elapsed_time = time.time() - self.elettronica_false_since
            # print(f"DEBUG CHECK | tempo : {elapsed_time}, warnign {self.trigger_warning}")
            if elapsed_time > 10:
                self.trigger_warning = True
                l.log_file(700)
        
        
    def effettua_calibrazione(self):
        self._log_thread_info("effettua_calibrazione")
        l.log_file(106, f" {self.bilancia.modbusI.address}")
        future = mg.calib_command(self.peso_calib.value(), self.bilancia.modbusI)
        future.add_done_callback(self.handle_calibrazione_completata)
    
    def handle_calibrazione_completata(self, future):
        self._log_thread_info("handle_calibrazione_completata")
        try:
            risult = future.result()
            self.calibrazione_completata_signal.emit(risult)
        except Exception as e:
            l.log_file(407, f"Errore durante la calibrazione: {e}")
    
    def update_calibrazione_ui(self, risult):
        self._log_thread_info("update_calibrazione_ui")
        if risult == 0: 
            print("all ok")
        else: 
            print("error")
            
    def effettua_tara(self):
        self._log_thread_info("effettua_tara")
        print(f"avvio tara {self.bilancia.modbusI.address}")
        future = mg.tare_command(self.bilancia.modbusI)
        future.add_done_callback(self.handle_tara_completata)
    
    def handle_tara_completata(self, future):
        self._log_thread_info("handle_tara_completata")
        try:
            risult = future.result()
            self.tara_completata_signal.emit(risult)
        except Exception as e:
            l.log_file(413, f"Errore durante la tara: {e}")
    
    def update_tara_ui(self, risult):
        self._log_thread_info("update_tara_ui")
        if risult == 0: 
            print("all ok")
        else: 
            print("error")
        
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(254,254,254))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()
    
    def load_stylesheet(self):
        file = QFile(f.get_style("bilancia.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)
    
    def _log_thread_info(self, function_name):
        """Log thread information for diagnostics."""
        current_thread = threading.current_thread()
        l.log_file(1000, f"DEBUG THREAD | {function_name} eseguito su thread: {current_thread.name} (ID: {current_thread.ident})")