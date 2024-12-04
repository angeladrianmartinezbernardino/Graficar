from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Ángulo de rotación.
angulo = 0

def inicializar():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo negro.
    glEnable(GL_DEPTH_TEST)  # Habilitar prueba de profundidad.

def display():
    global angulo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar buffers.
    glLoadIdentity()
    glTranslatef(-2.0, 2.0, -10.0)  # Trasladar la escena.

    # Organizar las figuras en una cuadrícula de 3x3.
    for i in range(3):
        for j in range(3):
            glPushMatrix()
            glTranslatef(j*2.0, -i*2.0, 0.0)  # Posicionar cada figura.
            # Reducir el tamaño de la figura del centro.
            if i == 1 and j == 1:
                glScalef(0.5, 0.5, 0.5)  # Reducir la figura central a la mitad.
            glRotatef(angulo, 1.0, 1.0, 1.0)  # Aplicar rotación.
            dibujar_figura(i*3 + j)
            glPopMatrix()
    glutSwapBuffers()

def dibujar_figura(indice):
    figuras = [
        glutSolidSphere,          # 0.
        glutSolidCube,            # 1.
        glutSolidCone,            # 2.
        glutSolidTorus,           # 3.
        glutSolidDodecahedron,    # 4.
        glutSolidOctahedron,      # 5.
        glutSolidTetrahedron,     # 6.
        glutSolidIcosahedron,     # 7.
        glutSolidTeapot           # 8.
    ]
    if indice < len(figuras):
        glColor3f(1.0, 0.0, 0.0)  # Color rojo.
        if figuras[indice] == glutSolidSphere:
            figuras[indice](0.5, 20, 20)
        elif figuras[indice] == glutSolidCube:
            figuras[indice](1.0)
        elif figuras[indice] == glutSolidCone:
            figuras[indice](0.5, 1.0, 20, 20)
        elif figuras[indice] == glutSolidTorus:
            figuras[indice](0.2, 0.5, 20, 20)
        elif figuras[indice] == glutSolidTeapot:
            figuras[indice](0.5)  # Especificamos el tamaño de la tetera.
        else:
            figuras[indice]()  # Las demás figuras no requieren parámetros.

def redimensionar(ancho, alto):
    if alto == 0:
        alto = 1
    ratio = ancho * 1.0 / alto
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, ratio, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def temporizador(valor):
    global angulo
    angulo += 1.0
    if angulo > 360.0:
        angulo -= 360.0
    glutPostRedisplay()
    glutTimerFunc(16, temporizador, 0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"9 Figuras GLUT Girando")
    inicializar()
    glutDisplayFunc(display)
    glutReshapeFunc(redimensionar)
    glutTimerFunc(0, temporizador, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
