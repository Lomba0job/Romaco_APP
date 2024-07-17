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

class GLWidget(QOpenGLWidget):
    rectDoubleClicked = pyqtSignal(int)

    def __init__(self, num_rectangles, parent=None):
        super().__init__(parent)
        self.num_rectangles = num_rectangles
        self.rect_positions = [
            QVector3D(-40, 0, 40),  # Top-left
            QVector3D(40, 0, 40),   # Top-right
            QVector3D(40, 0, -40),  # Bottom-left
            QVector3D(-40, 0, -40)  # Bottom-right
        ]
        self.rect_size = QVector3D(30.0, 10.0, 30.0)
        self.selected_rect = None
        self.last_pos = QPointF()
        self.camera_angle_x = 0
        self.camera_angle_y = 0
        self.camera_position_x = 0
        self.camera_position_y = 100
        self.camera_position_z = 400
        self.rotating_camera = False
        self.moving_camera = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

        self.model = self.load_obj(f.get_img("bilancia.obj"))
        self.vbo_vertices = None
        self.vbo_faces = None
        self.model_scale = self.calculate_scale()

    def load_obj(self, filepath):
        vertices = []
        faces = []
        with open(filepath, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    vertex = [float(x) for x in line.strip().split()[1:]]
                    # Adjust the axes
                    vertices.append([vertex[0], vertex[2], -vertex[1]])
                elif line.startswith('f '):
                    face = [int(vertex.split('/')[0]) for vertex in line.strip().split()[1:]]
                    faces.append(face)
        print("Loaded model with", len(vertices), "vertices and", len(faces), "faces.")
        return vertices, faces


    def calculate_scale(self):
        vertices, _ = self.model
        vertices = np.array(vertices)
        print("Vertices array shape:", vertices.shape)
        
        if vertices.size == 0:
            print("Vertices array is empty.")
            return 1.0

        min_coords = vertices.min(axis=0)
        max_coords = vertices.max(axis=0)
        dimensions = max_coords - min_coords
        print("Model dimensions:", dimensions)

        scale_x = self.rect_size.x() / dimensions[0]
        scale_y = self.rect_size.y() / dimensions[1]
        scale_z = self.rect_size.z() / dimensions[2]

        print(f"Calculated scales - X: {scale_x}, Y: {scale_y}, Z: {scale_z}")
        return min(scale_x, scale_y, scale_z)

    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        self.init_vbo()

    def init_vbo(self):
        vertices, faces = self.model

        vertices = np.array(vertices, dtype=np.float32)
        faces = np.array(faces, dtype=np.uint32) - 1

        print("Vertices buffer size:", vertices.nbytes)
        print("Faces buffer size:", faces.nbytes)

        self.vbo_vertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_vertices)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        print("Vertices VBO initialized.")

        self.vbo_faces = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo_faces)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)
        print("Faces VBO initialized.")

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(self.camera_position_x, self.camera_position_y, self.camera_position_z, 0, 0, 0, 0, 1, 0)
        glRotatef(self.camera_angle_x, 1, 0, 0)
        glRotatef(self.camera_angle_y, 0, 1, 0)

        self.drawPlane()

        for i in range(self.num_rectangles):
            self.drawModel(self.rect_positions[i])

    def drawPlane(self):
        glColor3f(0, 0, 0)
        glBegin(GL_LINES)
        grid_size = 100
        step = 5
        for i in range(-grid_size, grid_size + step, step):
            # Horizontal lines
            glVertex3f(i, -5, -grid_size)
            glVertex3f(i, -5, grid_size)
            # Vertical lines
            glVertex3f(-grid_size, -5, i)
            glVertex3f(grid_size, -5, i)
        glEnd()

    def drawModel(self, position):
        glPushMatrix()
        glTranslatef(position.x(), position.y(), position.z())
        glScalef(self.model_scale, self.model_scale, self.model_scale)

        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_vertices)
        glVertexPointer(3, GL_FLOAT, 0, None)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo_faces)
        glDrawElements(GL_TRIANGLES, len(self.model[1]) * 3, GL_UNSIGNED_INT, None)

        glDisableClientState(GL_VERTEX_ARRAY)
        glPopMatrix()

    def mousePressEvent(self, event):
        self.makeCurrent()
        self.last_pos = event.position()
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.moving_camera = True
        elif event.buttons() == Qt.MouseButton.RightButton:
            self.rotating_camera = True

    def mouseMoveEvent(self, event):
        if self.moving_camera:
            dx = (event.position().x() - self.last_pos.x()) / 5.0
            dy = (event.position().y() - self.last_pos.y()) / 5.0
            self.camera_position_x -= dx
            self.camera_position_y += dy
            self.last_pos = event.position()
        elif self.rotating_camera:
            dx = (event.position().x() - self.last_pos.x()) / 5.0
            dy = (event.position().y() - self.last_pos.y()) / 5.0
            self.camera_angle_y += dx
            self.camera_angle_x += dy
            self.last_pos = event.position()
        self.update()

    def mouseReleaseEvent(self, event):
        self.moving_camera = False
        self.rotating_camera = False

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.camera_position_z -= delta * 10
        self.camera_position_z = max(100, min(self.camera_position_z, 1000))
        self.update()