import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# De Ángel Adrián Martínez Bernardino y Luis Carlos Prieto Juárez.
# Definir la configuración inicial de la ventana.
Ancho, Altura = 1260, 600


# Función para inicializar PyOpenGL.
def Vistas():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(50, (Ancho / Altura), 0.1, 50.0)
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


# Función para dibujar un barco genérico basado en su longitud, posición y orientación.
def Dibujar_barco(Longitud, x, y, Orientacion):
    glBegin(GL_QUADS)
    for i in range(Longitud):
        if Orientacion == 'horizontal':
            glVertex3fv((x + i, 0, y))
            glVertex3fv((x + i, 0, y + 1))
            glVertex3fv((x + 1 + i, 0, y + 1))
            glVertex3fv((x + 1 + i, 0, y))
        else:  # orientacion == 'vertical'.
            glVertex3fv((x, 0, y + i))
            glVertex3fv((x, 0, y + 1 + i))
            glVertex3fv((x + 1, 0, y + 1 + i))
            glVertex3fv((x + 1, 0, y + i))
    glEnd()


def Dibujar_barco_1(x, y, orientacion):
    glColor3fv((0.0, 0.5647, 0.5647)) # Azul menta.
    Dibujar_barco(3, x, y, orientacion)  # Asumiendo que la longitud del barco 1 es 3.


def Dibujar_barco_2(x, y, orientacion):
    glColor3fv((0.6353, 0.1216, 0.0314)) # Rojo cereza.
    Dibujar_barco(3, x, y, orientacion)  # Asumiendo que la longitud del barco 2 es 3.


def Dibujar_barco_3(x, y, orientacion):
    glColor3fv((0.1451, 0.7098, 0.2039)) # Verde oscuro.
    Dibujar_barco(4, x, y, orientacion)  # Asumiendo que la longitud del barco 3 es 4.


# Modificación en la función principal para dibujar los barcos.
def Main():
    pygame.init()
    pygame.display.set_mode((Ancho, Altura), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Tablero isométrico para juego')
    Vistas()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Dibujar_grid()
        # Ejemplo de cómo colocar los barcos.
        Dibujar_barco_1(7, 0, 'horizontal')
        Dibujar_barco_2(3, 8, 'horizontal')
        Dibujar_barco_3(4, 4, 'horizontal')
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    Main()
