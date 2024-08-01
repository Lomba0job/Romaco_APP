from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPalette
from API import funzioni as f

class LogEntryWidget(QWidget):
    def __init__(self, date, weight, priority, priority_level):
        super().__init__()
        self.setFixedHeight(40)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 0, 10, 0)
        content_layout.setSpacing(0)
        
        # PESATA Label and Value
        date_label = QLabel("PESATA:")
        date_label.setObjectName("label")
        layout.addWidget(date_label)
        layout.addSpacing(10)
        date_value = QLabel(date)
        date_value.setObjectName("value")
        layout.addWidget(date_value)
        
        layout.addStretch()
        
        # PESO TOTALE Label and Value
        weight_label = QLabel("PESO TOTALE:")
        weight_label.setObjectName("label")
        layout.addWidget(weight_label)
        layout.addSpacing(10)
        weight_value = QLabel(weight)
        weight_value.setObjectName("value")
        layout.addWidget(weight_value)
        
        layout.addStretch()
        
        # PRIORITÁ Label and Value
        priority_label = QLabel("PRIORITÁ:")
        priority_label.setObjectName("label")
        layout.addWidget(priority_label)
        layout.addSpacing(10)
        priority_value = QLabel(priority)
        priority_value.setObjectName("value")
        layout.addWidget(priority_value)
        
        
        layout.addWidget(content_widget)
        
        color_widget = QWidget()
        color_widget.setFixedSize(40, 40)
        color_widget.setObjectName("colorIndicator")
        layout.addWidget(color_widget)
        
        self.setLayout(layout)
        # self.load_stylesheet()
        self.setAutoFillBackground(True)
        self.set_background_color(QColor(241, 241, 241))
        self.set_priority_color(color_widget, priority_level)
    
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
                border: none;
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
    
    def load_stylesheet(self):
        try:
            with open(f.get_style("log_ogg.qss"), "r") as file:
                additional_style = file.read()
                self.setStyleSheet(self.styleSheet() + additional_style)
        except Exception as e:
            print(f"Error loading stylesheet: {e}")