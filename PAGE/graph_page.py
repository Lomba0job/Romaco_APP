from PyQt6.QtWidgets import QWidget, QHBoxLayout
import platform


if platform.system() == "Linux":
    from CMP import rectangle_linux as r
else:
    from CMP import rectangle_univ as r

class Graph_page(QWidget):
    
    def __init__(self, master):
        super().__init__()
        
        w = QHBoxLayout()
        self.mast = master
        self.mast.setWindowTitle("Graph_page")
        self.glWidget = r.VTKWidget(num_rectangles=6)
        
        w.addWidget(self.glWidget)
        
        self.setLayout(w)

    def openDialog(self, rect_index):
        dialog = r.VTKWidget(self)
        dialog.exec()