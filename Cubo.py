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

# Posición inicial del cubo.
Posicion_cubo = [5, 5]  # Centro del tablero.

# Ángulo para la proyección isométrica (30 grados).
Angulo_Isometrico = math.radians(30)

# Función para inicializar PyOpenGL con ajuste a la ventana y perspectiva.
def Vistas():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cambiar a glOrtho y definir los planos near y far
    glOrtho(0, Eje_X_Programa, 0, Eje_Y_Programa, -100, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Función para convertir las coordenadas 3D en coordenadas isométricas.
def Isometrico3D(x, y, z):
    X_Isometrico = ((x - y) * (Tamaño_Casilla_X / 2))
    Y_Isometrico = ((x + y) * (Tamaño_Casilla_Y / 2)) - (z * Tamaño_Casilla_Y)
    # Ajustar con los márgenes
    X_Final = X_Isometrico + (Eje_X_Programa / 2)
    Y_Final = Y_Isometrico + Margen_Eje_Y_Programa_Respecto_Tablero_Isometrico
    return X_Final, Y_Final

# Función para dibujar el tablero.
def Dibujar_Grid():
    for i in range(Tablero_Eje_X):
        for j in range(Tablero_Eje_Y):
            Dibujar_Casilla(i, j)

# Función para dibujar una casilla.
def Dibujar_Casilla(x, y):
    X_isometrico, Y_isometrico = Isometrico3D(x, y, 0)
    Mitad_X = Tamaño_Casilla_X / 2
    Mitad_Y = Tamaño_Casilla_Y / 2
    z = -0.1  # Casillas ligeramente detrás del cubo
    # Dibujo de la casilla
    glColor3fv((0.70, 0.85, 0.90))  # Azul claro.
    glBegin(GL_QUADS)
    glVertex3f(X_isometrico, Y_isometrico, z)
    glVertex3f(X_isometrico + Mitad_X, Y_isometrico + Mitad_Y, z)
    glVertex3f(X_isometrico, Y_isometrico + Tamaño_Casilla_Y, z)
    glVertex3f(X_isometrico - Mitad_X, Y_isometrico + Mitad_Y, z)
    glEnd()
    # Dibujo de las líneas de la casilla
    glColor3fv((0.0, 0.0, 0.0))  # Líneas negras
    glBegin(GL_LINE_LOOP)
    glVertex3f(X_isometrico, Y_isometrico, z)
    glVertex3f(X_isometrico + Mitad_X, Y_isometrico + Mitad_Y, z)
    glVertex3f(X_isometrico, Y_isometrico + Tamaño_Casilla_Y, z)
    glVertex3f(X_isometrico - Mitad_X, Y_isometrico + Mitad_Y, z)
    glEnd()

# Función para dibujar el cubo.
def Dibujar_Cubo(x, y):
    # Definir los vértices del cubo en coordenadas 3D.
    vertices = [
        (x,     y,     0),  # Inferior frontal izquierdo
        (x+1,   y,     0),  # Inferior frontal derecho
        (x+1,   y,     1),  # Superior frontal derecho
        (x,     y,     1),  # Superior frontal izquierdo
        (x,     y+1,   0),  # Inferior trasero izquierdo
        (x+1,   y+1,   0),  # Inferior trasero derecho
        (x+1,   y+1,   1),  # Superior trasero derecho
        (x,     y+1,   1),  # Superior trasero izquierdo
    ]
    # Proyectar los vértices a coordenadas 2D (añadiendo Z=0)
    proyectados = [Isometrico3D(v[0], v[1], v[2]) + (0.0,) for v in vertices]
    # Definir las caras del cubo.
    caras = [
        (0, 1, 2, 3),  # Cara frontal
        (1, 5, 6, 2),  # Cara derecha
        (5, 4, 7, 6),  # Cara trasera
        (4, 0, 3, 7),  # Cara izquierda
        (3, 2, 6, 7),  # Cara superior
        (0, 1, 5, 4),  # Cara inferior (no visible)
    ]
    # Dibuja las caras del cubo
    glColor3fv((1, 0, 0))  # Rojo.
    glBegin(GL_QUADS)
    for cara in caras:
        for vertice in cara:
            glVertex3f(*proyectados[vertice])
    glEnd()
    # Dibuja las aristas del cubo.
    aristas = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Cara frontal
        (4, 5), (5, 6), (6, 7), (7, 4),  # Cara trasera
        (0, 4), (1, 5), (2, 6), (3, 7),  # Aristas laterales
    ]
    glColor3fv((1, 1, 1))  # Blanco para las aristas.
    glBegin(GL_LINES)
    for arista in aristas:
        glVertex3f(*proyectados[arista[0]])
        glVertex3f(*proyectados[arista[1]])
    glEnd()

# Función para mover el cubo.
def Mover_cubo(tecla, Posicion_cubo):
    if tecla == pygame.K_DOWN and Posicion_cubo[0] > 1:
        Posicion_cubo[0] -= 1
    if tecla == pygame.K_UP and Posicion_cubo[0] < Tablero_Eje_X:
        Posicion_cubo[0] += 1
    if tecla == pygame.K_LEFT and Posicion_cubo[1] < Tablero_Eje_Y:
        Posicion_cubo[1] += 1
    if tecla == pygame.K_RIGHT and Posicion_cubo[1] > 1:
        Posicion_cubo[1] -= 1

# Función principal del programa.
def Main():
    pygame.init()
    pygame.display.set_mode((Eje_X_Programa, Eje_Y_Programa), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Vista isométrica del tablero con el cubo movible')
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Fondo blanco
    Vistas()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                Mover_cubo(event.key, Posicion_cubo)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()  # Resetear la matriz de modelo-vista
        Dibujar_Grid()
        Dibujar_Cubo(Posicion_cubo[0], Posicion_cubo[1])
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    Main()
