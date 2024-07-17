import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def load_model(file):
    vertices = []
    faces = []
    with open(file) as f:
        for line in f:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('f '):
                face = [int(i.split('/')[0]) - 1 for i in line.strip().split()[1:]]
                faces.append(face)
    return vertices, faces

def draw_model(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    vertices, faces = load_model('/Users/lavoro/Documents/PROGETTI_LAVORO/Romaco_4/05_software/Romaco_APP/NLG00000021.obj')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_model(vertices, faces)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
