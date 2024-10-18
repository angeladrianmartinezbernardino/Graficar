from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

control_points = []

def CastleJau(input_points, t):
    l = len(input_points)
    if l == 0:
        return None
    if l == 1:
        return input_points[0]
    if t < 0.0 or t > 1.0:
        return None
    s = []
    for i in range(l - 1):
        p = (1.0 - t) * input_points[i] + t * input_points[i + 1]
        s.append(p.astype(float))  # Aseguramos que sea un array de floats.
    return CastleJau(s, t)

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Fondo blanco.
    glColor3f(0.0, 0.0, 0.0)  # Color negro para dibujar.
    glPointSize(5.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 640.0, 0.0, 480.0)  # Rango del sistema de coordenadas.

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)  # Color rojo para el polígono de control.
    glBegin(GL_LINE_STRIP)
    for point in control_points:
        glVertex2f(point[0], point[1])
    glEnd()
    glColor3f(0.0, 0.0, 1.0)  # Color azul para los puntos de control.
    glBegin(GL_POINTS)
    for point in control_points:
        glVertex2f(point[0], point[1])
    glEnd()
    if len(control_points) >= 2:
        # Dibujar la curva de Bézier
        glColor3f(0.0, 1.0, 0.0)  # Color verde para la curva.
        glBegin(GL_LINE_STRIP)
        for t in np.linspace(0.0, 1.0, num=100):
            p = CastleJau(control_points, t)
            if p is not None:
                glVertex2f(p[0], p[1])
        glEnd()
    glFlush()

def mouse(button, state, x, y):
    if state == GLUT_DOWN:
        viewport = glGetIntegerv(GL_VIEWPORT)
        win_height = viewport[3]
        opengl_y = win_height - y
        point = np.array([float(x), float(opengl_y)], dtype=float)  # Aseguramos que sean floats.

        if button == GLUT_LEFT_BUTTON:
            # Agregar punto de control
            control_points.append(point)
        elif button == GLUT_RIGHT_BUTTON:
            # Remover último punto de control si existe.
            if control_points:
                control_points.pop()
        glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Curva de Bézier usando el algoritmo de Casteljau")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMainLoop()

if __name__ == '__main__':
    main()
