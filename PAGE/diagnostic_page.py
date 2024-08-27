from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal, QThread, pyqtSlot, QTimer
from PyQt6.QtGui import QColor

import threading
from API import modbus_generico as mg, LOG as l 
import time
from CMP import Bilancia_diagno as b, Bilancia_diagno_deactive as bd

class StatusUpdateThread(QThread):
    status_updated = pyqtSignal()  # Segnale per aggiornare la UI
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(parent.update_status)
        self.update_interval = 5000  # 5 secondi

    def run(self):
        self.timer.start(self.update_interval)
        self.exec()  # Inizia il loop degli eventi per il thread
    
    def stop(self):
        self.timer.stop()
        self.quit()
        self.wait()

class DiagnosticWidget(QWidget):
    
    
    calibrazione_completata_signal = pyqtSignal(int)

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.setWindowTitle("RESPONSE ANALYZE APP")
        
        self.screen_width = self.master.screen_width 
        self.screen_height = self.master.screen_height
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.UI()
        v1 = QVBoxLayout()
        self.push = QPushButton()
        self.push.setText("ESEGUI LA TARA COMPLETA")
        self.push.setEnabled(False)
        self.push.clicked.connect(self.calib_all)
        self.push.setObjectName("pls")
        
        self.push.setMinimumWidth(int(self.screen_width * 0.5))
        self.push.setMaximumWidth(int(self.screen_width * 0.5))
        self.push.setMinimumHeight(int(self.screen_height * 0.1))
        self.push.setMaximumHeight(int(self.screen_height * 0.1))
        
        h0 = QHBoxLayout()
        h0.addStretch()
        h0.addWidget(self.push)
        h0.addStretch()
        
        v1.addSpacing(70)
        v1.addLayout(h0)
        v1.addStretch()
        v1.setContentsMargins(0, 0, 0, 0)
        v1.addLayout(self.main_layout)
        v1.addSpacing(10)
        self.setStyleSheet("""
            QWidget#bil{
                border: 1px solid grey;
                border-radius: 9px;
            }
            QPushButton#pls{
                border: 1px solid grey;
                background-color: #FFFFFF;
                color: #FD6363;
                font-size: 30px;
                border-radius: 10px;
            }
            QPushButton#pls1{
                border: 1px solid grey;
                background-color: #FD6363;
                color: #000000;
                font-size: 30px;
                border-radius: 10px;
            }
        """)
        self.setLayout(v1)
       
        self.setAutoFillBackground(True)
        self.set_background_color()
        
        # Inizializza il thread di aggiornamento dello stato
        self.status_thread = StatusUpdateThread(parent=self)
        self.status_thread.status_updated.connect(self.update_status)
        
        # Avvia il thread solo se ci sono bilance nella lista
        if len(self.master.lista_bilance) > 0:
            self.status_thread.start()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout is not None:
                        self.clearLayout(sub_layout)

    def update(self):
        current_layout = self.main_layout  # Ottieni il layout corrente del widget
        self.clearLayout(current_layout)  # Pulisci il layout corrente
        self.UI()  # Ricrea l'interfaccia utente
        if not self.status_thread.isRunning() and len(self.master.lista_bilance) > 0:
            self.status_thread.start()

    def UI(self):
        self.lista_ogg_attivi = []
        # print(f"DEBUG DIAGNO| {len(self.master.lista_bilance)}")
        for i in range(1, 7):
            if i <= len(self.master.lista_bilance):
                home_page = b.Bilancia(i, self.screen_width-10, self.screen_height-10, self.master.lista_bilance[i-1])
                home_page.setObjectName("weed")
                self.lista_ogg_attivi.append(home_page)
            else:
                home_page = bd.Bilancia(i, self.screen_width-10, self.screen_height-10)
                home_page.setObjectName("weed")
            
            if len(self.master.lista_bilance) > 0: 
                self.push.setEnabled(True)
                
            raggruppa = QWidget()
            l0 = QHBoxLayout()
            l0.setSpacing(0)
            l0.addWidget(home_page)
            l0.setContentsMargins(2, 2, 2, 2)
            raggruppa.setLayout(l0)
            
            raggruppa.setObjectName("bil")
            raggruppa.setContentsMargins(1, 1, 1, 1)
            
            self.main_layout.addWidget(raggruppa)
            
    @pyqtSlot()
    def update_status(self):
        if len(self.lista_ogg_attivi) != 0:
            for ogg in self.lista_ogg_attivi:
                ogg.update()
                if ogg.trigger_warning:
                    self.status_thread.stop()
                    print("DISTRUTTO")
                    self.master.disconnect()
                    self.push.setEnabled(False)
                    self.update()
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241,241,241))
        self.setPalette(p)
    
    def calib_all(self):
        self.push.setObjectName("pls1")
        self.push.setText("IN ELABORAZIONE")
        self._log_thread_info("calib_all")
        l.log_file(104)
        for b in self.master.lista_bilance:
            # print(f"avvio calibrazione {b.modbusI.address}")
            future = mg.tare_command(b.modbusI)
            future.add_done_callback(self.handle_calibrazione_completata)

    def handle_calibrazione_completata(self, future):
        self._log_thread_info("handle_calibrazione_completata")
        try:
            risult = future.result()
            self.calibrazione_completata_signal.emit(risult)
        except Exception as e:
            l.log_file(407, f" {e}")

    def update_calibrazione_ui(self, risult):
        self.push.setObjectName("pls")
        self._log_thread_info("update_calibrazione_ui")
        if risult == 0:
            l.log_file(4)
        else:
            l.log_file(405)
            QMessageBox.warning(self, "Tara Totale", "Errore")
            
            
    def _log_thread_info(self, function_name):
        """Log thread information for diagnostics."""
        current_thread = threading.current_thread()
        l.log_file(1000, f" | {function_name} eseguito su thread: {current_thread.name} (ID: {current_thread.ident})")