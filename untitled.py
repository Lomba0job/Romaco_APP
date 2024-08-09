import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QPointF, pyqtSignal, QTimer
from PyQt6.QtGui import QVector3D
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

from API import funzioni as f


def load_mtl(filepath):
    materials_info = {}
    current_material = None

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('newmtl '):
                current_material = line.split()[1]
                materials_info[current_material] = {}
            elif current_material:
                if line.startswith('Ka '):
                    materials_info[current_material]['Ka'] = line.split()[1:]
                elif line.startswith('Kd '):
                    materials_info[current_material]['Kd'] = line.split()[1:]
                elif line.startswith('Ks '):
                    materials_info[current_material]['Ks'] = line.split()[1:]
                elif line.startswith('Ns '):
                    materials_info[current_material]['Ns'] = line.split()[1]
                elif line.startswith('Tr '):
                    materials_info[current_material]['Tr'] = line.split()[1]

    return materials_info

def get_material_color(material_name, materials_info):
    material_info = materials_info.get(material_name, {})
    kd = material_info.get('Kd', ['0.8', '0.8', '0.8'])  # Default color
    return [float(c) for c in kd]

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertices = []
        self.faces = []
        self.face_colors = []
        self.model_loaded = False

        # Timer per aggiornare il rendering
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)

        # Carica i dati del modello
        self.load_model(f.get_img('bilancia_def.obj'), f.get_img('mat.mtl'))

    def load_model(self, obj_file, mtl_file):
        materials_info = load_mtl(mtl_file)
        current_material = None

        with open(obj_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('v '):  # Definizione di un vertice
                    vertex = [float(coord) for coord in line.split()[1:]]
                    self.vertices.append(vertex)
                elif line.startswith('f '):  # Definizione di una faccia
                    face = [int(vertex.split('/')[0]) - 1 for vertex in line.split()[1:]]
                    self.faces.append(face)
                    if current_material:
                        self.face_colors.append(get_material_color(current_material, materials_info))
                elif line.startswith('usemtl '):  # Cambio di materiale
                    current_material = line.split()[1]

        if self.vertices and self.faces:
            self.model_loaded = True
        else:
            print("Failed to load model or no faces/vertices found.")

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

        if self.model_loaded:
            self.draw_model()
        else:
            print("No model loaded to render.")

    def draw_model(self):
        glBegin(GL_TRIANGLES)
        for face, color in zip(self.faces, self.face_colors):
            glColor3f(*color)
            for vertex_idx in face:
                glVertex3f(*self.vertices[vertex_idx])
        glEnd()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = GLWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())