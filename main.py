import sys
from PyQt6.QtCore import Qt, QEvent, QFile, QTextStream, QDateTime, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar
)
from PyQt6.QtGui import QPixmap, QAction

from PAGE import home_page as h, launcher_page as l, salva_peso_page as s, log_page as lo, diagnostic_page as d
from CMP import navbar as nv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.state = 0
        self.setWindowTitle("RESPONSE ANALYZE APP")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.create_pages()

        self.navbar = nv.NavbarWidget(self)
        self.setMenuWidget(self.navbar)
        self.navbar.setVisible(True)  # Nascondi la barra di navigazione all'avvio

        self.pages = {
            self.navbar.home_button: 1,
            self.navbar.log_button: 3, 
            self.navbar.diagno_button: 4
        }
        for button, index in self.pages.items():
            button.clicked.connect(lambda checked=True, index=index: self.change_page(index))

        self.navbar.settings_button_clicked.connect(lambda: self.change_page(4))

        self.change_page(1)  # Initialize to the launcher page

    def create_pages(self):
        # Launcher Page
        self.lista_bilance = []
        self.launcher_page = l.LauncherWidget()
        self.launcher_page.finished.connect(self.on_launcher_finished)
        self.central_widget.addWidget(self.launcher_page)

        # Rubrica Page
        self.rubrica_page = h.Home_Page(self)
        self.central_widget.addWidget(self.rubrica_page)
        
        self.salva_peso = s.SalvaPesoWidget(self)
        self.central_widget.addWidget(self.salva_peso)
        
        self.log = lo.LogPage(self)
        self.central_widget.addWidget(self.log)
        
        self.diagno = d.DiagnosticWidget(self)
        self.central_widget.addWidget(self.diagno)
        
    def launcher_call(self):
        self.navbar.setVisible(False)   #Nascondi La navbar
        self.change_page(0)  # Passa alla pagina rubrica
        
    def save_call(self):
        self.navbar.setVisible(False)   #Nascondi La navbar
        self.change_page(2)  # Passa alla pagina rubrica

    def on_launcher_finished(self):
        self.navbar.setVisible(True)  # Mostra la barra di navigazione
        self.lista_bilance = self.launcher_page.lista_bilance
        print(f"DEBUG MAIN {len(self.lista_bilance)}")
        self.rubrica_page.initUI()
        self.diagno.update()
        self.change_page(1)  # Passa alla pagina rubrica
        
    def disconnect(self):
        self.lista_bilance = []
        self.rubrica_page.reinitUI()

    def change_page(self, index):
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