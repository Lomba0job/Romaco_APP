import sys
from PyQt6.QtCore import Qt, QFile, QTextStream, QSize, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QFrame, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar, 
    QDoubleSpinBox, QFileDialog, QMessageBox

    
)
import shutil
from PyQt6.QtGui import QPixmap, QAction, QIcon, QColor
import os 

from PAGE import setting_page as s
from API import funzioni as f, LOG as l

from CMP import puls_livello1 as p, puls_livello1_interni as pi, messaggi as m

class Livello1(QWidget):

    def __init__(self, master):
        super().__init__()
        self.master:s.Settings = master
        
        
        self.main_layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        
        self.home_page() #indice 0
        self.log_page() #indice 1
        self.db_page()  #indice 2
        
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)
        
        
        self.setLayout(self.main_layout)
        self.setAutoFillBackground(True)
        self.set_background_color()
        
        #self.setMaximumSize(self.master.master.screen_width,(self.master.master.screen_height))  # Imposta una dimensione fissa per la finestra principale
        # self.stacked_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(254,254,254))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("settings.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)
    
    def home_page(self):
        
        home_widget = QWidget()
        home_layout = QHBoxLayout()
        home_widget.setLayout(home_layout)
        
        p1 = p.ClickableWidget(f.get_img("DB_F.png"),     "Operazioni Database") 
        p1.clicked.connect(self.db_operatione)
        p2 = p.ClickableWidget(f.get_img("LOG_DATA.png"), "Operazioni DataLog") 
        p2.clicked.connect(self.dataLog_operatione)
        
        home_layout.addStretch()
        home_layout.addWidget(p1)
        home_layout.addSpacing(50)
        home_layout.addWidget(p2)
        home_layout.addStretch()
        
        self.stacked_widget.addWidget(home_widget)
        
    def db_page(self):
        
        home_widget = QWidget()
        home_layout = QHBoxLayout()
        home_widget.setLayout(home_layout)
        
        p1 = pi.ClickableWidget(f.get_img("trash.png"),     "Elimina dati database") 
        p1.clicked.connect(lambda: self.svuota_file(f.get_db()))
        p2 = pi.ClickableWidget(f.get_img("share.png"), "Esporta dati database") 
        p2.clicked.connect(self.show_save_db)
        
        home_layout.addStretch()
        home_layout.addWidget(p1)
        home_layout.addSpacing(50)
        home_layout.addWidget(p2)
        home_layout.addStretch()
        
        self.stacked_widget.addWidget(home_widget)
        
    def log_page(self):
        
        home_widget = QWidget()
        home_layout = QHBoxLayout()
        home_widget.setLayout(home_layout)
        
        p1 = pi.ClickableWidget(f.get_img("trash.png"), "Elimina DataLog") 
        p1.clicked.connect(self.svuota_log)
        p2 = pi.ClickableWidget(f.get_img("share.png"), "Esporta DataLog") 
        p2.clicked.connect(self.show_save_log)
        
        home_layout.addStretch()
        home_layout.addWidget(p1)
        home_layout.addSpacing(50)
        home_layout.addWidget(p2)
        home_layout.addStretch()
        
        self.stacked_widget.addWidget(home_widget)
         
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
                    
    def home(self):
        self.stacked_widget.setCurrentIndex(0)
        self.master.contro_label(1)
    
    
    def dataLog_operatione(self):
        self.stacked_widget.setCurrentIndex(1)
        self.master.contro_label(4)
    
    
    def db_operatione(self):
        self.stacked_widget.setCurrentIndex(2)
        self.master.contro_label(5)
    
    def svuota_log(self):
        self.svuota_file(f.get_app_log())
        self.svuota_file(f.get_thread_log())
        
    
    def show_save_db(self):
        
        # Prima, scegli il file da copiare
        db= f.get_db()
        
        default_name = "database.db"
        destination_file, _ = QFileDialog.getSaveFileName(self, 
                                                         "Salva File Concatenato Come", 
                                                         default_name, 
                                                         "Log files (*.db);;Tutti i file (*)",
                                                         )
        if destination_file:
            # Assicurarsi che il file salvato abbia l'estensione .log
            if not destination_file.endswith('.db'):
                destination_file += '.db'
            
            try:      
                # Leggi il contenuto dei due file
                with open(db, 'r') as file1, open(destination_file, 'w') as outfile:
                    outfile.write(file1.read())
                      # Aggiunge una nuova linea tra i contenuti dei due file
                    
                
                l.log_file(17, f"{destination_file}")
                
                self.show_success_message(f"Salvataggio del file \"{destination_file}\" db termianta con successo")
            except Exception as e:
                self.show_error_message(f"Errore durante il salvataggio del file: {e}")
                
            
    def show_save_log(self):
        # Prima, scegli il file da copiare
        log1 = f.get_app_log()
        log2 = f.get_thread_log()

        default_name = "concatenated_log.log"
        destination_file, _ = QFileDialog.getSaveFileName(self, 
                                                         "Salva File Concatenato Come", 
                                                         default_name, 
                                                         "Log files (*.log);;Tutti i file (*)",
                                                         )
        if destination_file:
            # Assicurarsi che il file salvato abbia l'estensione .log
            if not destination_file.endswith('.log'):
                destination_file += '.log'

            try:
                # Check if the source files exist and are readable
                if not os.path.exists(log1):
                    raise FileNotFoundError(f"File not found: {log1}")
                if not os.path.exists(log2):
                    raise FileNotFoundError(f"File not found: {log2}")

                # Open files and write content
                with open(log1, 'r') as file1, open(log2, 'r') as file2, open(destination_file, 'w') as outfile:
                    outfile.write(file1.read())
                    outfile.write("\n")  # Aggiunge una nuova linea tra i contenuti dei due file
                    outfile.write(file2.read())

                l.log_file(15, f"{destination_file}")
                self.show_success_message(f"Concatenazione e salvataggio del file \"{destination_file}\" log termianta con successo")
            except Exception as e:
                # Log the error and show an error message
                l.log_file(418, f"Errore durante la concatenazione dei file: {e}")
                self.show_error_message(f"Errore durante la concatenazione dei file: {e}")

    
    def svuota_file(self, percorso_file):
        try:
            # Apri il file in modalità di scrittura ('w') per svuotarlo
            with open(percorso_file, 'w') as file:
                pass  # Non scriviamo nulla, lasciamo semplicemente il file vuoto
            if percorso_file == f.get_db():
                self.master.master.ripristino_db()
                l.log_file(18)
            else:
                l.log_file(16)
            self.show_success_message(f"Il contenuto del file '{percorso_file}' è stato eliminato.")
        except Exception as e:
            self.show_error_message("Si è verificato un errore durante l'eliminazione del contenuto del file: {e}")
    
    def show_success_message(self, messaggio):
        ico = QIcon(f.get_img("close.png"))
        myModal = m.QCustomModals.SuccessModal(
            title="salvataggio eseguito",  # Title of the modal dialog
            parent=self,  # Parent widget to which the modal belongs
            position='top-right',  # Position to display the modal dialog
            closeIcon=ico,  # Path to the close icon image
            description=messaggio,  # Description text displayed in the modal dialog
            isClosable=False,  # Whether the modal dialog is closable (True or False)
            duration=3000  # Duration (in milliseconds) for which the modal dialog remains visible
        )

        # Show the modal
        myModal.show()
        
    def show_error_message(self, messaggio):
        ico = QIcon(f.get_img("close.png"))
        myModal = m.QCustomModals.ErrorModal(
            title="salvataggio eseguito",  # Title of the modal dialog
            parent=self,  # Parent widget to which the modal belongs
            position='top-right',  # Position to display the modal dialog
            closeIcon=ico,  # Path to the close icon image
            description=messaggio,  # Description text displayed in the modal dialog
            isClosable=False,  # Whether the modal dialog is closable (True or False)
            duration=3000  # Duration (in milliseconds) for which the modal dialog remains visible
        )

        # Show the modal
        myModal.show()
        
 