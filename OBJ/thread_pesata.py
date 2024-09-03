import concurrent.futures
import threading
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy, QProgressBar
from PyQt6.QtCore import Qt, QFile, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QSize
from PyQt6.QtGui import QColor, QPalette
import time 

from API import modbus_generico as mb, LOG as l 



class PesataThread(QThread):
    pesata_completata = pyqtSignal(list)  # Segnale emesso al completamento della pesata

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.pesi_bilance = []

    def run(self):
        self._log_thread_info("run")
        self.start_time = time.time()
        QThread.msleep(500)  # Aspetta 500 millisecondi prima di iniziare il ciclo di pesatura

        # print(f"DEBUG PESATA | bilance {len(self.master.lista_bilance)}")

        for bilancia in self.master.lista_bilance:
            self.set_weight_question(bilancia)
            
    def set_weight_question(self, bilancia):
        self._log_thread_info("set_weight_question")
        future_peso_tot = mb.set_richesta_peso(bilancia.modbusI)
        future_peso_tot.add_done_callback(lambda f: self.get_weight_for_bilancia(f, bilancia))


    def get_weight_for_bilancia(self, future, bilancia):
        if future != 1:
            self._log_thread_info("get_weight_for_bilancia")
            l.log_file(999, f"richiesta peso bilancia{bilancia.modbusI.address}")
            start_bilancia_time = time.time()

            future_peso_tot = mb.get_totWeight(bilancia.modbusI)
            future_peso_tot.add_done_callback(lambda f: self.handle_peso_tot(f, bilancia, start_bilancia_time))
        else:
            self.pesata_completata.emit(self.pesi_bilance)
             
    def handle_peso_tot(self, future, bilancia, start_bilancia_time):
        self._log_thread_info("handle_peso_tot")
        l.log_file(999, f"peso TOTALE bilancia{bilancia.modbusI.address}")
        try:
            pesotot = future.result()
            end_peso_tot = time.time()
            # print(f"DEBUG PESATA | peso TOT {pesotot} {bilancia.modbusI.address}  completed in {end_peso_tot - start_bilancia_time:.4f} seconds ")
            if pesotot != -1:
                l.log_file(999, f"richiesto peso celle bilancia{bilancia.modbusI.address}")
                future_cell_weight = mb.get_cellWeight(bilancia.modbusI)
                future_cell_weight.add_done_callback(lambda f: self.handle_cell_weight(f, bilancia, pesotot, start_bilancia_time))
            else:
                self.handle_pesata_result(None, bilancia, start_bilancia_time)
        except Exception as e:
            l.log_file(412, f" {e}")
            self.handle_pesata_result(None, bilancia, start_bilancia_time)

    def handle_cell_weight(self, future, bilancia, pesotot, start_bilancia_time):
        self._log_thread_info("handle_cell_weight")
        try:
            peso = future.result()
            l.log_file(999, f"peso celle bilancia{bilancia.modbusI.address}")
            end_cell_time = time.time()
            # print(f"DEBUG PESATA check | pesi {peso} completed in {end_cell_time - start_bilancia_time:.4f} seconds ")
            s = peso[0]
            # print(f"DEBUG PESATA check | pesi {peso}, primo {s}")
            warn = False
            if self.master.binario.get_lettura:
                for p in peso:
                    l.log_file(113, f"differenza interna max {self.master.binario.get_lettura_val() * 1000}")
                    if abs(p - s) > (self.master.binario.get_lettura_val() * 1000):  # SOTTOCHIAVE IMPOSTAZIONE
                        warn = True  
                        
            # print(f"DEBUG PESATA check | war {warn}")
            if not warn:
                l.log_file(3)
                self.handle_pesata_result(pesotot, bilancia, start_bilancia_time)
            else:
                l.log_file(403)
                self.handle_pesata_result(None, bilancia, start_bilancia_time)
        except Exception as e:
            l.log_file(403, f" {e}")
            self.handle_pesata_result(None, bilancia, start_bilancia_time)

    def handle_pesata_result(self, result, bilancia, start_bilancia_time):
        self._log_thread_info("handle_pesata_result")
        end_bilancia_time = time.time()
        if result is not None:
            l.log_file(999,f"DEBUG PESATA TIME | Bilancia {bilancia.modbusI.address} completed in {end_bilancia_time - start_bilancia_time:.4f} seconds")
            self.pesi_bilance.append(result)
        else:
            l.log_file(999,f"DEBUG PESATA TIME | Bilancia {bilancia.modbusI.address} completed in {end_bilancia_time - start_bilancia_time:.4f} seconds (failed or warning)")
            self.pesata_completata.emit(self.pesi_bilance)
            
        if len(self.pesi_bilance) == len(self.master.lista_bilance):
            self.pesata_completata.emit([peso for peso in self.pesi_bilance if peso is not None])

            end_time = time.time()
            l.log_file(999, f"PESATA TIME | Total pesata process completed in {end_time - self.start_time:.4f} seconds")

            self.pesata_completata.emit(self.pesi_bilance)  # Emit the signal with the result

    def _log_thread_info(self, function_name):
        """Log thread information for diagnostics."""
        current_thread = threading.current_thread()
        l.log_file(1000, f"DEBUG THREAD | {function_name} eseguito su thread: {current_thread.name} (ID: {current_thread.ident})")
