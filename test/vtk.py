import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import vtkRenderer
import vtk

os.environ['QT_QPA_PLATFORM'] = 'xcb'
os.environ['VTK_USE_X'] = '1'

class SimpleVTKWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.layout.addWidget(self.vtkWidget)

        self.renderer = vtkRenderer()
        self.renderer.SetBackground(1, 1, 1)
        self.render_window = self.vtkWidget.GetRenderWindow()
        self.render_window.AddRenderer(self.renderer)

        self.interactor = self.render_window.GetInteractor()
        self.interactor.Initialize()
        self.interactor.Start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setCentralWidget(SimpleVTKWidget())
    main_window.resize(800, 600)
    main_window.show()
    sys.exit(app.exec())