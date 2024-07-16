import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QPointF, pyqtSignal, QTimer
from PyQt6.QtGui import QVector3D
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class RectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rectangle Dialog")
        layout = QVBoxLayout()
        button = QPushButton("Close")
        button.clicked.connect(self.close)
        layout.addWidget(button)
        self.setLayout(layout)

class GLWidget(QOpenGLWidget):
    rectDoubleClicked = pyqtSignal(int)

    def __init__(self, num_rectangles, parent=None):
        super().__init__(parent)
        self.num_rectangles = num_rectangles
        self.rect_positions = [
            QVector3D(-40, 0, 40),  # Top-left
            QVector3D(40, 0, 40),   # Top-right
            QVector3D(40, 0, -40), # Bottom-left
            QVector3D(-40, 0, -40)   # Bottom-right
        ]
        self.rect_size = QVector3D(20.0, 5.0, 20.0)
        self.selected_rect = None
        self.last_pos = QPointF()
        self.camera_angle_x = 0
        self.camera_angle_y = 0
        self.rotating_camera = False
        self.zoom_distance = 400  # Initialize the zoom distance
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def initializeGL(self):
        # Initialize OpenGL settings
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        # Adjust the viewport and projection matrix
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 1, 1000)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        # Clear the buffer and set the camera position
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotatef(self.camera_angle_x, 1, 0, 0)
        glRotatef(self.camera_angle_y, 0, 1, 0)
        gluLookAt(0, 100, self.zoom_distance, 0, 0, 0, 0, 1, 0)  # Set camera with zoom distance

        self.drawPlane()

        for i, pos in enumerate(self.rect_positions):
            self.drawRectangle(pos.x(), pos.y(), pos.z())
            if i > 0:
                self.drawArrow(self.rect_positions[i - 1], pos)

    def drawPlane(self):
        # Draw the ground plane
        glColor3f(0.8, 0.8, 0.8)
        glBegin(GL_QUADS)
        glVertex3f(-100, -5, -100)
        glVertex3f(100, -5, -100)
        glVertex3f(100, -5, 100)
        glVertex3f(-100, -5, 100)
        glEnd()

    def drawRectangle(self, x, y, z):
        # Draw a filled rectangle
        w, h, d = self.rect_size.x() / 2, self.rect_size.y() / 2, self.rect_size.z() / 2
        glPushMatrix()
        glTranslatef(x, y, z)

        glBegin(GL_QUADS)
        glColor3f(0.0, 1.0, 0.0)
        # Front face
        glVertex3f(-w, -h, d)
        glVertex3f(w, -h, d)
        glVertex3f(w, h, d)
        glVertex3f(-w, h, d)
        glEnd()

        glBegin(GL_QUADS)
        # Back face
        glVertex3f(-w, -h, -d)
        glVertex3f(w, -h, -d)
        glVertex3f(w, h, -d)
        glVertex3f(-w, h, -d)
        glEnd()

        glBegin(GL_QUADS)
        # Top face
        glVertex3f(-w, h, d)
        glVertex3f(w, h, d)
        glVertex3f(w, h, -d)
        glVertex3f(-w, h, -d)
        glEnd()

        glBegin(GL_QUADS)
        # Bottom face
        glVertex3f(-w, -h, d)
        glVertex3f(w, -h, d)
        glVertex3f(w, -h, -d)
        glVertex3f(-w, -h, -d)
        glEnd()

        glBegin(GL_QUADS)
        # Left face
        glVertex3f(-w, -h, d)
        glVertex3f(-w, h, d)
        glVertex3f(-w, h, -d)
        glVertex3f(-w, -h, -d)
        glEnd()

        glBegin(GL_QUADS)
        # Right face
        glVertex3f(w, -h, d)
        glVertex3f(w, h, d)
        glVertex3f(w, h, -d)
        glVertex3f(w, -h, -d)
        glEnd()

        glPopMatrix()

    def drawArrow(self, start, end):
        # Draw an arrow from one rectangle to the next
        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        glVertex3f(start.x(), start.y(), start.z())
        glVertex3f(end.x(), end.y(), end.z())
        glEnd()

    def mousePressEvent(self, event):
        # Handle mouse press events for selecting rectangles and rotating camera
        self.last_pos = event.position()
        if event.buttons() == Qt.MouseButton.LeftButton:
            print("premuto tasto sinistro")
            for i, pos in enumerate(self.rect_positions):
                if (pos.x() - self.rect_size.x() / 2 <= (self.last_pos.x() - self.width() / 2) <= pos.x() + self.rect_size.x() / 2 and
                    pos.y() - self.rect_size.y() / 2 <= -(self.last_pos.y() - self.height() / 2) <= pos.y() + self.rect_size.y() / 2):
                    print("interno")
                    self.selected_rect = i
                    break
        elif event.buttons() == Qt.MouseButton.RightButton:
            print("premuto tasto destro")
            self.rotating_camera = True

    def mouseMoveEvent(self, event):
        # Handle mouse move events for dragging rectangles and rotating camera
        if self.selected_rect is not None:
            dx = (event.position().x() - self.last_pos.x()) / 10.0
            dy = -(event.position().y() - self.last_pos.y()) / 10.0
            self.rect_positions[self.selected_rect] += QVector3D(dx, dy, 0)
            self.last_pos = event.position()
        elif self.rotating_camera:
            dx = (event.position().x() - self.last_pos.x()) / 5.0
            dy = (event.position().y() - self.last_pos.y()) / 5.0
            self.camera_angle_y += dx
            self.camera_angle_x += dy
            self.last_pos = event.position()
        self.update()

    def mouseReleaseEvent(self, event):
        # Handle mouse release events to stop dragging or rotating
        self.selected_rect = None
        self.rotating_camera = False

    def mouseDoubleClickEvent(self, event):
        # Handle mouse double click events to signal rectangle double click
        for i, pos in enumerate(self.rect_positions):
            if (pos.x() - self.rect_size.x() / 2 <= (event.position().x() - self.width() / 2) <= pos.x() + self.rect_size.x() / 2 and
                pos.y() - self.rect_size.y() / 2 <= -(event.position().y() - self.height() / 2) <= pos.y() + self.rect_size.y() / 2):
                self.rectDoubleClicked.emit(i)
                print(f"Rectangle {i} double-clicked")
                break
    
    def wheelEvent(self, event):
        # Handle mouse wheel events for zooming in and out
        delta = event.angleDelta().y() / 120
        self.zoom_distance -= delta * 10
        self.zoom_distance = max(100, min(self.zoom_distance, 1000))  # Set zoom limits
        self.update()