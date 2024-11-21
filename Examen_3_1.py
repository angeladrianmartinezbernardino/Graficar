import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Variable global para la posición vertical de la esfera
y_pos = 0.5  # La esfera comienza justo encima del suelo

def init():
    # Configuración del fondo y modos de renderizado
    glClearColor(0.5, 0.5, 0.5, 1.0)  # Fondo gris
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Configuración de la luz
    light_pos = [1.0, 1.0, 1.0, 0.0]
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    # Configuración del material de la esfera
    material_ambient = [1.0, 0.0, 0.0, 1.0]  # Color rojo
    material_diffuse = [1.0, 0.0, 0.0, 1.0]
    material_specular = [1.0, 1.0, 1.0, 1.0]
    material_shininess = [50.0]

    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(0.0, 1.0, 5.0,  # Posición de la cámara
              0.0, 0.0, 0.0,  # Punto al que mira
              0.0, 1.0, 0.0)  # Vector "up"

    # Dibujar el suelo
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor3f(0.1, 0.1, 0.1)  # Color negro con un leve reflejo
    glBegin(GL_QUADS)
    glVertex3f(-1.0, 0.0, -1.0)  # Aumentar el tamaño del suelo
    glVertex3f(1.0, 0.0, -1.0)
    glVertex3f(1.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.0, 1.0)
    glEnd()
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Aplicar traslación vertical a la esfera
    glTranslatef(0.0, y_pos, 0.0)

    # Dibujar la esfera más pequeña
    glutSolidSphere(0.5, 50, 50)  # Radio reducido a 0.5

    glutSwapBuffers()

def reshape(width, height):
    if height == 0:
        height = 1
    aspect = width / height

    glViewport(0, 0, width, height)

    # Configuración de la proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, aspect, 1.0, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard(key, x, y):
    if key == b'\x1b':  # Tecla ESC para salir
        sys.exit()

def specialKeys(key, x, y):
    global y_pos
    if key == GLUT_KEY_UP:
        y_pos += 0.1  # Mover hacia arriba
    elif key == GLUT_KEY_DOWN:
        y_pos -= 0.1  # Mover hacia abajo
        # Evitar que la esfera traspase el suelo
        if y_pos - 0.5 < 0.0:  # 0.5 es el radio de la esfera
            y_pos = 0.5  # Posición mínima para que la esfera toque el suelo
    glutPostRedisplay()

def main():
    # Inicialización de GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Esfera Iluminada con Suelo Negro")

    init()

    # Registro de funciones de devolución de llamada
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialKeys)

    # Bucle principal
    glutMainLoop()

if __name__ == "__main__":
    main()
