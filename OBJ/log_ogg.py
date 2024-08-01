from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPalette
from API import funzioni as f

class LogEntryWidget(QWidget):
    def __init__(self, date, weight, priority, priority_level):
        super().__init__()
        self.setFixedHeight(40)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(0)
        
        date_label = QLabel(f"PESATA: {date}")
        date_label.setObjectName("date")
        layout.addWidget(date_label)
        
        layout.addStretch()
        
        weight_label = QLabel(f"PESO TOTALE: {weight}")
        weight_label.setObjectName("weight")
        layout.addWidget(weight_label)
        
        layout.addStretch()
        
        priority_label = QLabel(f"PRIORITÁ: {priority}")
        priority_label.setObjectName("priority")
        layout.addWidget(priority_label)
        
        color_widget = QWidget()
        color_widget.setFixedSize(40, 40)
        color_widget.setObjectName("colorIndicator")
        self.set_priority_color(color_widget, priority_level)
        layout.addWidget(color_widget)
        
        self.setLayout(layout)
        self.load_stylesheet()
        self.set_background_color(QColor(241, 241, 241))
        self.set_priority_color(color_widget, priority_level)
        
    
    def set_priority_color(self, widget, priority_level):
        colors = {
            0: "#B0F29D",  # Verde chiaro per priorità bassa
            1: "#E8D984",  # Giallo per priorità media
            2: "#EB7171"   # Rosso chiaro per priorità alta
        }
        color = colors.get(priority_level, "#FFFFFF")  # Bianco come colore di default
        widget.setStyleSheet(f"background-color: {color};")
    
    def set_background_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
    def load_stylesheet(self):
        try:
            with open(f.get_style("log_ogg.qss"), "r") as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")