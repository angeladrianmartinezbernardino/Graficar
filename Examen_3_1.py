from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

# Inicialización
def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    # Configuración de la luz
    light_pos = [1.0, 1.0, 1.0, 1.0]  # Posición de la luz
    light_amb = [0.2, 0.2, 0.2, 1.0]  # Luz ambiental
    light_diff = [1.0, 1.0, 1.0, 1.0]  # Luz difusa
    light_spec = [1.0, 1.0, 1.0, 1.0]  # Luz especular

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_amb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diff)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_spec)

    # Color del material
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(0.0, 0.0, 5.0,  # Posición de la cámara
              0.0, 0.0, 0.0,  # Punto al que mira
              0.0, 1.0, 0.0)  # Vector arriba

    # Dibujar el plano
    glPushMatrix()
    glColor3f(0.0, 0.3, 0.3)  # Color del plano
    glTranslatef(0.0, -0.5, 0.0)
    glScalef(3.0, 0.1, 2.0)
    glutSolidCube(1.0)  # Representar el plano como un cubo escalado
    glPopMatrix()

    # Dibujar la esfera
    glPushMatrix()
    glColor3f(0.8, 0.1, 0.1)  # Color de la esfera
    glTranslatef(0.0, 0.5, 0.0)
    glutSolidSphere(0.5, 50, 50)  # Radio, slices, stacks
    glPopMatrix()

    glutSwapBuffers()

def reshape(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OpenGL Iluminacion")
    init()
    glutDisplayFunc(draw)
    glutReshapeFunc(reshape)
    glutMainLoop()

if __name__ == "__main__":
    main()
