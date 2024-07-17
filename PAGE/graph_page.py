from PyQt6.QtWidgets import QWidget, QHBoxLayout


from CMP import rectangle as r

class Graph_page(QWidget):
    
    def __init__(self, master):
        super().__init__()
        
        w = QHBoxLayout()
        self.mast = master
        self.mast.setWindowTitle("Graph_page")
        self.glWidget = r.GLWidget(num_rectangles=6)
        
        w.addWidget(self.glWidget)
        
        self.setLayout(w)

    def openDialog(self, rect_index):
        dialog = r.RectDialog(self)
        dialog.exec()