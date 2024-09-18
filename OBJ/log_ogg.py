from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPalette
from API import funzioni as f, API_db as db


class DetailsDialog(QDialog):
    def __init__(self, entry_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dettagli Pesata")
        self.setFixedSize(600, 600)
        
        layout = QVBoxLayout(self)
        
        # Tabella per mostrare i dettagli
        self.table = QTableWidget(11, 2)  # -11 campi (peso_totale, peso_b1, peso_b2, etc.)
        self.table.setHorizontalHeaderLabels(["Campo", "Valore"])
        layout.addWidget(self.table)
        
        # Pulsante per chiudere la finestra
        close_button = QPushButton("Chiudi")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        # Carica i dettagli della riga dal database
        self.load_details(entry_id)

    def load_details(self, entry_id):
        # Recupera i dati dal database usando l'ID
        entry_data = db.get_by_id(entry_id)
        if entry_data:
            fields = ["Peso Totale", "Peso Bilancia 1", "Peso Bilancia 2", "Peso Bilancia 3", "Peso Bilancia 4", "Peso Bilancia 5", "Peso Bilancia 6", "Descrizione", "Priorità", "Data", "Nome"]
            values = [entry_data.get('peso_totale'), entry_data.get('peso_b1'), entry_data.get('peso_b2'), 
                      entry_data.get('peso_b3'), entry_data.get('peso_b4'), entry_data.get('peso_b5'), 
                      entry_data.get('peso_b6'), entry_data.get('desc'), entry_data.get('priority'), 
                      entry_data.get('data'), entry_data.get('name')]
            print(values)
            for i, (field, value) in enumerate(zip(fields, values)):
                self.table.setItem(i, 0, QTableWidgetItem(field))
                self.table.setItem(i, 1, QTableWidgetItem(str(value)))
                
class LogEntryWidget(QWidget):
    def __init__(self, id, sdate, peso_totale, name, priority, parent=None):
        super().__init__(parent)
        self.id = id
        self.date = sdate
        self.peso_totale = peso_totale
        self.name = name
        self.priority = priority
        date_str = str(sdate)  # Assicurati che date sia una stringa
        print(f"{date_str}, {peso_totale}, {name}, {priority}")
        self.setFixedHeight(40)
        self.setContentsMargins(0, 0, 0, 0)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        content_widget = QWidget(self)
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # PESATA Label and Value
        date_label = QLabel("PESATA:")
        date_label.setObjectName("label")
        content_layout.addWidget(date_label)
        content_layout.addSpacing(10)
        
        date_value = QLabel(date_str)
        date_value.setObjectName("value")
        content_layout.addWidget(date_value)
        
        content_layout.addStretch()
        
        # PESO TOTALE Label and Value
        weight_label = QLabel("PESO TOTALE:")
        weight_label.setObjectName("label")
        content_layout.addWidget(weight_label)
        content_layout.addSpacing(10)
        
        weight_value = QLabel(str(peso_totale))
        weight_value.setObjectName("value")
        content_layout.addWidget(weight_value)
        
        content_layout.addStretch()
        
        # PRIORITÁ Label and Value
        priority_label = QLabel("NOME:")
        priority_label.setObjectName("label")
        content_layout.addWidget(priority_label)
        content_layout.addSpacing(10)
        
        priority_value = QLabel(name)
        self.set_fixed_length_text(priority_value, name, 25)
        priority_value.setObjectName("value")
        priority_value.setMinimumWidth(120)
        priority_value.setMaximumWidth(120)
        content_layout.addWidget(priority_value)
        content_layout.addSpacing(20)
        
        layout.addWidget(content_widget)
        
        
        # Color indicator
        color_widget = QWidget()
        color_widget.setFixedSize(40, 40)
        color_widget.setObjectName("colorIndicator")
        layout.addWidget(color_widget)
        
        self.setLayout(layout)
        self.setAutoFillBackground(True)
        self.set_background_color(QColor(255, 255, 255))
        self.set_priority_color(color_widget, priority)
    
    
    def set_priority_color(self, widget, priority_level):
        colors = {
            0: "#B0F29D",  # Verde chiaro per priorità bassa
            1: "#E8D984",  # Giallo per priorità media
            2: "#EB7171"   # Rosso chiaro per priorità alta
        }
        color = colors.get(priority_level, "#FFFFFF")  # Bianco come colore di default
        widget.setStyleSheet(f"""
            background-color: {color};
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
        """)
    
    def set_background_color(self, color):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {color.name()};
                
            }}
            QLabel#label {{
                color: #5D5D5D;
                font-size: 14px;
                font-weight: bold;
            }}
            QLabel#value {{
                color: #EB7171;
                font-size: 14px;
                font-weight: bold;
            }}
        """)
    def set_fixed_length_text(self, label, text, length):
        if len(text) > length:
            text = text[:length]
        else:
            text = text.ljust(length)
        label.setText(text)
        
    def load_stylesheet(self):
        try:
            with open(f.get_style("log_ogg.qss"), "r") as file:
                additional_style = file.read()
                self.setStyleSheet(self.styleSheet() + additional_style)
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
            
    def mousePressEvent(self, event):
        # Apri la finestra di dialogo quando il widget viene cliccato
        self.show_details_dialog()

    def show_details_dialog(self):
        # Mostra una finestra di dialogo con i dettagli della riga selezionata
        details_dialog = DetailsDialog(self.id)
        details_dialog.exec()