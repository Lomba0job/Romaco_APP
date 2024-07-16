import sys
from PyQt6.QtCore import Qt, QEvent, QFile, QTextStream, QDateTime, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar
)
from PyQt6.QtGui import QPixmap,  QAction

from PAGE import home_page as h

from CMP import navbar as nv

import sys

    
class MainWindow(QMainWindow):
    def __init__(self):
        
        self.state = 0
        super().__init__()
        self.setWindowTitle("RESPONSE ANALYZE APP")
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Imposta le dimensioni della finestra principale
        self.setGeometry(0, 0, screen_width, screen_height)


        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.create_pages()

        self.navbar = nv.NavbarWidget(self)
        self.setMenuWidget(self.navbar)

        # Connect buttons to change pages and highlight active button
        self.pages = {
            self.navbar.home_button: 0
        }
        for button, index in self.pages.items():
            button.clicked.connect(lambda checked=True, index=index: self.change_page(index))

        self.navbar.settings_button_clicked.connect(lambda: self.change_page(4))

        self.change_page(0)  # Initialize to the first page

    def create_pages(self):
        # Rubrica Page
        self.rubrica_page = h.Home_Page(self)
        self.central_widget.addWidget(self.rubrica_page)


    def change_page(self, index):
        if self.state != 0 and index == 0:
            self.rubrica_page.reload_data()

        self.state = index
        self.central_widget.setCurrentIndex(index)
        for button, button_index in self.pages.items():
            if button_index == index:
                rect = button.rect()
                button.setProperty("active", True)
                button.setStyle(button.style())  # Refresh style
            else:
                button.setProperty("active", False)
                button.setStyle(button.style())  # Refresh style



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())