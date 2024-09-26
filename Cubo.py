import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Dimensiones de la ventana y del tablero.
Eje_X_Programa = 424
Eje_Y_Programa = 254
Margen_Eje_X_Programa_Respecto_Tablero_Isometrico = 18
Margen_Eje_Y_Programa_Respecto_Tablero_Isometrico = 15
Tamaño_Casilla_X = (Eje_X_Programa - (2 * Margen_Eje_X_Programa_Respecto_Tablero_Isometrico)) / 10
Tamaño_Casilla_Y = (Eje_Y_Programa - (2 * Margen_Eje_Y_Programa_Respecto_Tablero_Isometrico)) / 10
Tablero_Eje_X = 10
Tablero_Eje_Y = 10

# Ángulo para la proyección isométrica (30 grados).
Angulo_Isometrico = math.radians(30)

# Función para inicializar PyOpenGL con ajuste a la ventana y perspectiva.
def Vistas():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, Eje_X_Programa, 0, Eje_Y_Programa)  # Proyección ortográfica ajustada al tamaño de la ventana.
    glMatrixMode(GL_MODELVIEW)

# Función para convertir las coordenadas 2D del tablero en coordenadas isométricas.
def Isometrico(x, y):
    # Cálculo de las coordenadas isométricas.
    X_Isometrico = ((Tablero_Eje_X - 1 - y) - (Tablero_Eje_X - 1 - x)) * (Tamaño_Casilla_X / 2)
    Y_Isometrico = ((Tablero_Eje_X - 1 - x) + (Tablero_Eje_X - 1 - y)) * (Tamaño_Casilla_Y / 2)
    # Ajustar con los márgenes
    X_Final = X_Isometrico + (Eje_X_Programa / 2)
    Y_Final = Y_Isometrico + Margen_Eje_Y_Programa_Respecto_Tablero_Isometrico
    return X_Final, Y_Final

# Función para dibujar el tablero (con líneas negras y casillas de fondo azul claro).
def Dibujar_Grid():
    for i in range(Tablero_Eje_X):
        for j in range(Tablero_Eje_Y):
            Dibujar_Casilla(i, j)

# Función para dibujar una casilla en una posición (x, y) en la vista isométrica.
def Dibujar_Casilla(x, y):
    X_isometrico, Y_isometrico = Isometrico(x, y)
    Mitad_X = Tamaño_Casilla_X / 2
    Mitad_Y = Tamaño_Casilla_Y / 2
    # Dibujo de la casilla (color de fondo azul claro).
    glColor3fv((0.70, 0.85, 0.90))  # Azul claro.
    glBegin(GL_QUADS)
    glVertex3f(X_isometrico, Y_isometrico, 0.0)
    glVertex3f(X_isometrico + Mitad_X, Y_isometrico + Mitad_Y, 0.0)
    glVertex3f(X_isometrico, Y_isometrico + Tamaño_Casilla_Y, 0.0)
    glVertex3f(X_isometrico - Mitad_X, Y_isometrico + Mitad_Y, 0.0)
    glEnd()
    # Dibujo de las líneas de la casilla (color de las líneas negras).
    glColor3fv((0.0, 0.0, 0.0))  # Líneas negras
    glBegin(GL_LINE_LOOP)
    glVertex3f(X_isometrico, Y_isometrico, 0.0)
    glVertex3f(X_isometrico + Mitad_X, Y_isometrico + Mitad_Y, 0.0)
    glVertex3f(X_isometrico, Y_isometrico + Tamaño_Casilla_Y, 0.0)
    glVertex3f(X_isometrico - Mitad_X, Y_isometrico + Mitad_Y, 0.0)
    glEnd()

# Función principal del programa.
def Main():
    pygame.init()
    pygame.display.set_mode((Eje_X_Programa, Eje_Y_Programa), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Vista isométrica del tablero con el cubo movible')
    glClearColor(1.0, 1.0, 1.0, 1.0) # Cambiar el fondo a blanco
    Vistas()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Dibujar_Grid()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    Main()
