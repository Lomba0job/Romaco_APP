import sys
from PyQt6.QtCore import Qt, QEvent, QFile, QTextStream, QDateTime, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QDialog, QGridLayout, QStackedWidget, QMenuBar
)
from PyQt6.QtGui import QPixmap,  QAction

from PAGE import import_page as i, rubrica as r, test_main as t, settings_page as s, rubrica_azienda as a

from CMP import navbar as nv
from API import funzioni_base as f
import sys

def qt_object_properties(qt_object: object) -> dict:
    """
    Create a dictionary of property names and values from a QObject.
    
    :param qt_object: The QObject to retrieve properties from.
    :type qt_object: object
    :return: Dictionary with format
        {'name': property_name, 'value': property_value}
    :rtype: dict
    """
    properties: list = []
    
    # Returns a list of QByteArray.
    button_properties: list = qt_object.dynamicPropertyNames()
    
    for prop in button_properties:
        # Decode the QByteArray into a string.
        name: str = str(prop, 'utf-8')
    
        # Get the property value from the button.
        value: str = qt_object.property(name)
    
        properties.append({'name': name, 'value': value})
    
    return properties
    
class MainWindow(QMainWindow):
    def __init__(self):
        f.boot()
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
            self.navbar.rubrica_button: 0,
            self.navbar.azienda_button: 1,
            self.navbar.inserisci_button: 2,
            self.navbar.test_button: 3
        }
        for button, index in self.pages.items():
            button.clicked.connect(lambda checked=True, index=index: self.change_page(index))

        self.navbar.settings_button_clicked.connect(lambda: self.change_page(4))

        self.change_page(0)  # Initialize to the first page

    def create_pages(self):
        # Rubrica Page
        self.rubrica_page = r.RubricaPage()
        self.central_widget.addWidget(self.rubrica_page)

        self.azienda_page = a.RubricaAzzPage()
        self.central_widget.addWidget(self.azienda_page)
        # Inserisci Page
        inserisci_page = i.FileMover()
        self.central_widget.addWidget(inserisci_page)

        # Test Page
        test_page = t.widget_test()
        self.central_widget.addWidget(test_page)

        # Settings Page
        settings_page = s.SettingsPage()
        self.central_widget.addWidget(settings_page)

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