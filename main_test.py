import sys
from PyQt6.QtCore import Qt, QEvent, QFile, QTextStream, QDateTime, pyqtSignal, QRect, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar
)
from PyQt6.QtGui import QPixmap, QAction, QGuiApplication, QColor


from API import funzioni as f 
from PAGE import home_page as h, launcher_page as l, salva_peso_page as s, log_page as lo
from CMP import navbar as nv, Bilancia_diagno as b, Bilancia_diagno_deactive as bd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle("Diagnostica")
        self.setWindowTitle("RESPONSE ANALYZE APP")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        # Set the central widget
        
        central_widget = QWidget()
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        v1 = QVBoxLayout(central_widget)

        # Create and add 6 instances of Home_Page
        for i in range(1, 7):
            if i < 5:
                home_page = b.Bilancia(i, self.screen_width-10, self.screen_height-10)
                home_page.setObjectName("weed")
            else:
                home_page = bd.Bilancia(i, self.screen_width-10, self.screen_height-10)
                home_page.setObjectName("weed")
                
            raggruppa = QWidget()
            l0 = QHBoxLayout()
            l0.setSpacing(0)
            l0.addWidget(home_page)
            l0.setContentsMargins(2,2,2,2)
            raggruppa.setLayout(l0)
            
            
            raggruppa.setObjectName("bil")
            raggruppa.setContentsMargins(1,1,1,1)
            
            main_layout.addWidget(raggruppa)
            
            
        self.setStyleSheet("""
            QWidget#bil{
                border: 1px solid grey;
                border-radius: 9px;
            }
        """)
            
        v1.addStretch()
        v1.setContentsMargins(0,0,0,0)
        v1.addLayout(main_layout)
        v1.addSpacing(10)
        
        self.setCentralWidget(central_widget)
        self.setAutoFillBackground(True)
        self.set_background_color()
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241,241,241))
        self.setPalette(p)
        # Load the stylesheet
        
        
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())