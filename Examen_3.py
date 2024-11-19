from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Variables para la posición y color
angle = 0.0


def init():
    glEnable(GL_DEPTH_TEST)  # Habilitar el test de profundidad
    glEnable(GL_LIGHTING)  # Habilitar iluminación
    glEnable(GL_LIGHT0)  # Habilitar la fuente de luz 0
    glEnable(GL_COLOR_MATERIAL)  # Habilitar material por color
    glShadeModel(GL_SMOOTH)  # Suavizar el sombreado

    # Configurar la luz
    light_position = [1.0, 1.0, 1.0, 1.0]
    light_diffuse = [1.0, 0.5, 0.5, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)


def draw_sphere():
    # Dibujar una esfera roja
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Color rojo
    glutSolidSphere(0.5, 50, 50)
    glPopMatrix()


def draw_cube():
    # Dibujar un cubo como base
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)  # Color gris
    glScalef(1.5, 0.5, 1.0)
    glutSolidCube(1.0)
    glPopMatrix()


def display():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configurar la cámara
    gluLookAt(0.0, 1.5, 3.0,  # Posición de la cámara
              0.0, 0.0, 0.0,  # Punto de enfoque
              0.0, 1.0, 0.0)  # Vector hacia arriba

    # Rotación animada de la escena
    glRotatef(angle, 0.0, 1.0, 0.0)

    # Dibujar las figuras
    draw_cube()
    glTranslatef(0.0, 0.75, 0.0)
    draw_sphere()

    glutSwapBuffers()


def update(value):
    global angle
    angle += 1.0
    if angle > 360:
        angle -= 360
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Illuminated Sphere")
    init()
    glutDisplayFunc(display)
    glutTimerFunc(16, update, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
