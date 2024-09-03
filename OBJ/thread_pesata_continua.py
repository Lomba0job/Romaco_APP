import concurrent.futures
import threading
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy, QProgressBar
from PyQt6.QtCore import Qt, QFile, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QSize
from PyQt6.QtGui import QColor, QPalette
import time 

from API import modbus_generico as mb

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

        print(f"DEBUG PESATA | bilance {len(self.master.lista_bilance)}")

        for bilancia in self.master.lista_bilance:
            self.set_weight_question(bilancia)
            
    def set_weight_question(self, bilancia):
        self._log_thread_info("set_weight_question")
        future_peso_tot = mb.set_richesta_peso(bilancia.modbusI)
        future_peso_tot.add_done_callback(lambda f: self.get_weight_for_bilancia(f, bilancia))


    def get_weight_for_bilancia(self, future, bilancia):
        if future != 1:
            self._log_thread_info("get_weight_for_bilancia")
            start_bilancia_time = time.time()

            future_peso_tot = mb.get_totWeight(bilancia.modbusI)
            future_peso_tot.add_done_callback(lambda f: self.handle_peso_tot(f, bilancia, start_bilancia_time))
        else:
            self.pesata_completata.emit(self.pesi_bilance)
            
    def handle_peso_tot(self, future, bilancia, start_bilancia_time):
        self._log_thread_info("handle_peso_tot")
        try:
            pesotot = future.result()
            end_peso_tot = time.time()
            # print(f"DEBUG PESATA | peso TOT {pesotot} {bilancia.modbusI.address}  completed in {end_peso_tot - start_bilancia_time:.4f} seconds ")
            if pesotot != -1:
                future_cell_weight = mb.get_cellWeight(bilancia.modbusI)
                future_cell_weight.add_done_callback(lambda f: self.handle_cell_weight(f, bilancia, pesotot, start_bilancia_time))
            else:
                self.handle_pesata_result(None, bilancia, start_bilancia_time)
        except Exception as e:
            print(f"Errore durante la lettura del peso totale: {e}")
            self.handle_pesata_result(None, bilancia, start_bilancia_time)

    def handle_cell_weight(self, future, bilancia, pesotot, start_bilancia_time):
        self._log_thread_info("handle_cell_weight")
        try:
            peso = future.result()
            end_cell_time = time.time()
            print(f"DEBUG PESATA check | pesi {peso} completed in {end_cell_time - start_bilancia_time:.4f} seconds ")
            # Restituiamo il peso totale e i pesi delle singole celle senza effettuare il controllo di discostamento
            self.handle_pesata_result([pesotot] + peso, bilancia, start_bilancia_time)
        except Exception as e:
            print(f"Errore durante la lettura dei pesi delle celle: {e}")
            self.handle_pesata_result(None, bilancia, start_bilancia_time)

    def handle_pesata_result(self, result, bilancia, start_bilancia_time):
        self._log_thread_info("handle_pesata_result")
        end_bilancia_time = time.time()
        if result is not None:
            print(f"DEBUG PESATA TIME | Bilancia {bilancia.modbusI.address} completed in {end_bilancia_time - start_bilancia_time:.4f} seconds")
        else:
            print(f"DEBUG PESATA TIME | Bilancia {bilancia.modbusI.address} completed in {end_bilancia_time - start_bilancia_time:.4f} seconds (failed or warning)")
        # Append a tuple (bilancia.id, result) to the list
        self.pesi_bilance.append((bilancia.modbusI.address, result))

        # Check if all bilance have completed their pesata
        if len(self.pesi_bilance) == len(self.master.lista_bilance):
            # Sort the pesi_bilance list by bilancia.id
            self.pesi_bilance.sort(key=lambda x: x[0])

            # Extract just the results, ordered by bilancia.id
            ordered_results = [result for _, result in self.pesi_bilance]

            end_time = time.time()
            print(f"DEBUG PESATA TIME | Total pesata process completed in {end_time - self.start_time:.4f} seconds")

            # Emit the signal with the ordered result
            self.pesata_completata.emit(ordered_results)

    def _log_thread_info(self, function_name):
        """Log thread information for diagnostics."""
        current_thread = threading.current_thread()
        print(f"DEBUG THREAD | {function_name} eseguito su thread: {current_thread.name} (ID: {current_thread.ident})")