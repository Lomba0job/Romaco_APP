from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont, QCursor, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QFile, QTextStream

from API import funzioni as f

class ClickableWidget(QWidget):
    clicked = pyqtSignal()  # Signal emitted when the widget is clicked

    def __init__(self, image_path, text, parent=None):
        super().__init__(parent)

        # Layout for the entire widget
        layout = QVBoxLayout()

        # Image Label
        self.image_label = QLabel(self)
        ico = QPixmap(image_path)
        self.image_label.setPixmap(QPixmap(ico).scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        # self.image_label.setFixedWidth(150)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Text Label
        self.text_label = QLabel(text, self)
        self.text_label.setObjectName("testo_puls1")
        # Sub-layout to hold text and image
        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)
        layout.addStretch()

        self.setLayout(layout)

        # Set cursor to hand cursor when hovering over the widget
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAutoFillBackground(True)
        self.set_background_color()
        
        
    
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()  # Emit the clicked signal when the widget is clicked

