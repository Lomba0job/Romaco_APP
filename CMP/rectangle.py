import sys
from PyQt6.QtWidgets import QApplication, QOpenGLWidget, QDialog, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer
from PyQt6.QtGui import QVector3D
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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
        self.rect_positions = [QVector3D(i * 2.0, i * 1.5, 0) for i in range(num_rectangles)]
        self.rect_size = QVector3D(2.0, 1.0, 0)
        self.selected_rect = None
        self.last_pos = QPoint()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 15, 0, 0, 0, 0, 1, 0)

        for i, pos in enumerate(self.rect_positions):
            self.drawRectangle(pos.x(), pos.y())
            if i > 0:
                self.drawArrow(self.rect_positions[i - 1], pos)

    def drawRectangle(self, x, y):
        glPushMatrix()
        glTranslatef(x, y, 0)
        glScalef(2, 1, 1)
        glBegin(GL_QUADS)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(-1, -1)
        glVertex2f(1, -1)
        glVertex2f(1, 1)
        glVertex2f(-1, 1)
        glEnd()
        glPopMatrix()

    def drawArrow(self, start, end):
        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        glVertex3f(start.x(), start.y(), start.z())
        glVertex3f(end.x(), end.y(), end.z())
        glEnd()

    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        for i, pos in enumerate(self.rect_positions):
            if (pos.x() - self.rect_size.x() / 2 <= self.last_pos.x() <= pos.x() + self.rect_size.x() / 2 and
                    pos.y() - self.rect_size.y() / 2 <= self.last_pos.y() <= pos.y() + self.rect_size.y() / 2):
                self.selected_rect = i
                break

    def mouseMoveEvent(self, event):
        if self.selected_rect is not None:
            dx = (event.x() - self.last_pos.x()) / 50.0
            dy = -(event.y() - self.last_pos.y()) / 50.0
            self.rect_positions[self.selected_rect] += QVector3D(dx, dy, 0)
            self.last_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.selected_rect = None

    def mouseDoubleClickEvent(self, event):
        for i, pos in enumerate(self.rect_positions):
            if (pos.x() - self.rect_size.x() / 2 <= event.x() <= pos.x() + self.rect_size.x() / 2 and
                    pos.y() - self.rect_size.y() / 2 <= event.y() <= pos.y() + self.rect_size.y() / 2):
                self.rectDoubleClicked.emit(i)
                break
