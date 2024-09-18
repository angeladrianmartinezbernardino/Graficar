import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Dimensiones de la ventana y del tablero
Ancho, Altura = 424, 254
Margen_X = 18
Margen_Y = 15
Tamaño_Casilla_Ancho = (Ancho - (2 * Margen_X)) / 10  # Ancho de las casillas
Tamaño_Casilla_Alto = (Altura - (2 * Margen_Y)) / 10  # Alto de las casillas
Tablero_Ancho = 10  # Número de casillas en el tablero
Tablero_Alto = 10

# Ángulo para la proyección isométrica (30 grados)
angulo_isometrico = math.radians(30)

# Función para inicializar PyOpenGL con ajuste a la ventana y perspectiva
def Vistas():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, Ancho, 0, Altura)  # Proyección ortográfica ajustada al tamaño de la ventana
    glMatrixMode(GL_MODELVIEW)

# Función para convertir las coordenadas 2D del tablero en coordenadas isométricas
def isometrico(x, y):
    # Cálculo de las coordenadas isométricas
    x_iso = (x - y) * (Tamaño_Casilla_Ancho / 2)
    y_iso = (x + y) * (Tamaño_Casilla_Alto / 2)

    # Ajustar con los márgenes
    x_final = x_iso + (Ancho / 2)
    y_final = y_iso + Margen_Y

    return x_final, y_final

# Función para dibujar el tablero (con líneas negras y casillas de fondo azul claro)
def Dibujar_grid():
    for i in range(Tablero_Ancho):
        for j in range(Tablero_Alto):
            Dibujar_casilla(i, j)

# Función para dibujar una casilla en una posición (x, y) en la vista isométrica
def Dibujar_casilla(x, y):
    x_iso, y_iso = isometrico(x, y)

    # Dibujo de la casilla (color de fondo azul claro)
    glColor3fv((0.678, 0.847, 0.902))  # Azul claro
    glBegin(GL_QUADS)
    glVertex2f(x_iso, y_iso)
    glVertex2f(x_iso + Tamaño_Casilla_Ancho / 2, y_iso + Tamaño_Casilla_Alto / 2)
    glVertex2f(x_iso, y_iso + Tamaño_Casilla_Alto)
    glVertex2f(x_iso - Tamaño_Casilla_Ancho / 2, y_iso + Tamaño_Casilla_Alto / 2)
    glEnd()

    # Dibujo de las líneas de la casilla (color de las líneas negras)
    glColor3fv((0.0, 0.0, 0.0))  # Líneas negras
    glBegin(GL_LINE_LOOP)
    glVertex2f(x_iso, y_iso)
    glVertex2f(x_iso + Tamaño_Casilla_Ancho / 2, y_iso + Tamaño_Casilla_Alto / 2)
    glVertex2f(x_iso, y_iso + Tamaño_Casilla_Alto)
    glVertex2f(x_iso - Tamaño_Casilla_Ancho / 2, y_iso + Tamaño_Casilla_Alto / 2)
    glEnd()

# Datos de los barcos, incluyendo orientación
barcos = [
    {"dimensiones": (3, 1), "coordenadas": (9, 7), "orientacion": "horizontal"},  # Barco 1 en (J, 8)
    {"dimensiones": (3, 1), "coordenadas": (1, 3), "orientacion": "horizontal"},  # Barco 2 en (B, 4)
    {"dimensiones": (4, 1), "coordenadas": (5, 4), "orientacion": "horizontal"}  # Barco 3 en (F, 5)
]

# Función para dibujar un barco en una posición (x, y) con orientación
def Dibujar_barco(barco):
    x, y = barco["coordenadas"]
    casillas_x, casillas_y = barco["dimensiones"]
    orientacion = barco["orientacion"]

    # Dibujo del barco con orientación (horizontal o vertical)
    glColor3fv((1.0, 0.0, 0.0))  # Rojo para los barcos
    glBegin(GL_QUADS)

    # Para orientación horizontal
    if orientacion == "horizontal":
        for i in range(casillas_x):
            x_actual, y_actual = isometrico(x + i, y)
            glVertex2f(x_actual, y_actual)
            glVertex2f(x_actual + Tamaño_Casilla_Ancho / 2, y_actual + Tamaño_Casilla_Alto / 2)
            glVertex2f(x_actual, y_actual + Tamaño_Casilla_Alto)
            glVertex2f(x_actual - Tamaño_Casilla_Ancho / 2, y_actual + Tamaño_Casilla_Alto / 2)

    # Para orientación vertical
    elif orientacion == "vertical":
        for i in range(casillas_y):
            x_actual, y_actual = isometrico(x, y + i)
            glVertex2f(x_actual, y_actual)
            glVertex2f(x_actual + Tamaño_Casilla_Ancho / 2, y_actual + Tamaño_Casilla_Alto / 2)
            glVertex2f(x_actual, y_actual + Tamaño_Casilla_Alto)
            glVertex2f(x_actual - Tamaño_Casilla_Ancho / 2, y_actual + Tamaño_Casilla_Alto / 2)

    glEnd()

# Función para dibujar todos los barcos
def Dibujar_barcos():
    for barco in barcos:
        Dibujar_barco(barco)

# Función principal del programa
def Main():
    pygame.init()
    pygame.display.set_mode((Ancho, Altura), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Vista isométrica del tablero con barcos')

    # Cambiar el fondo a blanco
    glClearColor(1.0, 1.0, 1.0, 1.0)

    Vistas()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Dibujar_grid()
        Dibujar_barcos()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    Main()
