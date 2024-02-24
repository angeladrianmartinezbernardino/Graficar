import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# De Ángel Adrián Martínez Bernardino.
# Definir la configuración inicial de la ventana.
width, height = 1260, 600


# Función para inicializar PyOpenGL.
def Vistas():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(50, (width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(5, 10, -10, 0, 0, 0, 0, 1, 0)


# Función para dibujar el tablero isométrico.
def Dibujar_grid():
    glBegin(GL_LINES)
    # Dibuja las líneas horizontales.
    for i in range(11):
        if i == 0 or i == 10:
            glColor3fv((1, 1, 1))  # Líneas blancas.
        else:
            glColor3fv((1, 1, 1))  # Líneas blancas.
        glVertex3fv((i, 0, 0))
        glVertex3fv((i, 0, 10))
    # Dibuja las líneas verticales.
    for j in range(11):
        if j == 0 or j == 10:
            glColor3fv((1, 1, 1))  # Líneas blancas.
        else:
            glColor3fv((1, 1, 1))  # Líneas blancas.
        glVertex3fv((0, 0, j))
        glVertex3fv((10, 0, j))
    glEnd()


# Función principal.
def Main():
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Tablero isométrico para juego')
    Vistas()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Dibujar_grid()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    Main()
